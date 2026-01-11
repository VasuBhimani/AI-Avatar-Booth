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


MAIL_USERNAME=os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = ''



# Database table schema
# DATABASE_SCHEMA = """
# CREATE DATABASE IF NOT EXISTS acd_data;
# USE acd_data;

# CREATE TABLE IF NOT EXISTS users (
#     id VARCHAR(50) PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL,
#     flag BOOLEAN DEFAULT FALSE
# );
