from dotenv import load_dotenv
import os

load_dotenv()
DB_CONFIG = {'host': os.getenv('DB_HOST'),
             'user': os.getenv('DB_USER'),
             'password': os.getenv('DB_PASSWORD'),
             'database': os.getenv('DB_DEMO_DATABASE')
             if os.getenv('APP_STATUS') == 'DEMO'
             else os.getenv('DB_DATABASE')
             }
