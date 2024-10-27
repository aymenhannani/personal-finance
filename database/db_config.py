import os

DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'your_username',
    'password': 'your_password',
    'dbname': 'finance_db'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:" \
               f"{DATABASE_CONFIG['password']}@" \
               f"{DATABASE_CONFIG['host']}:" \
               f"{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"