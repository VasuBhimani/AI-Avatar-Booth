from dotenv import load_dotenv
load_dotenv() 
import os
import threading
from flask import Flask, render_template, request, jsonify, url_for
import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'
load_dotenv() 
task_done = False
task_lock = threading.Lock()

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:5000/webhook")
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="qr_scanner_pool",
        pool_size=5,
        **DB_CONFIG
    )
    print("✅ Database pool ready")
except Exception as e:
    print(f"❌ DB connection failed: {e}")
    connection_pool = None

def get_db_connection():
    if connection_pool:
        return connection_pool.get_connection()
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM acddata WHERE id = %s", (user_id,)) 
        user = cursor.fetchone()
        cursor.close()
        return user
    finally:
        conn.close()

@app.route('/')
def index():
    global task_done
    task_done = False
    return render_template('index.html')

@app.route('/loading')
def loading_page():
    return render_template('loading.html')

@app.route('/api/scan', methods=['POST'])
def scan_qr():
    try:
        qr_data = request.json.get('qr_data', '')
        parts = dict(item.split(':', 1) for item in qr_data.split('|') if ':' in item)
        user_id, name = parts.get('id'), parts.get('n')

        if not user_id or not name:
            return jsonify({'success': False, 'message': 'Invalid QR data'}), 400
        # Check DB
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if not user.get('flag'):
            return jsonify({'success': False, 'message': 'Flag is false'}), 403
        def send_webhook():
            try:
                webhook_data = {
                    'id': user_id,
                    'name': name,
                    'email': user.get('email'),
                    'message': 'x0x0x0'
                }
                requests.post(WEBHOOK_URL, json=webhook_data, timeout=3)
            except Exception as e:
                print(f"Webhook error: {e}")
        threading.Thread(target=send_webhook, daemon=True).start()
        return jsonify({'success': True, 'redirect_url': '/loading'})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        global task_done
        data = request.json
        if data.get('message') == "xxxx":
            with task_lock:
                task_done = True
            return jsonify({"status": "success", "redirect_url": "/"})
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/check_task_status', methods=['GET'])
def check_task_status():
    global task_done
    with task_lock:
        done = task_done
    if done:
        return jsonify({'status': 'complete', 'redirect': url_for('index')})
    return jsonify({'status': 'pending'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
