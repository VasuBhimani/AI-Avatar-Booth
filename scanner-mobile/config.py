import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'acd_data'),
    'charset': 'utf8mb4',
    'autocommit': True
}




