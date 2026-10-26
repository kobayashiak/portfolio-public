from dotenv import load_dotenv
import os
from db.game_database import GameDatabase
load_dotenv()


client_id = os.getenv('STEAM_ID')
client_name = os.getenv('DOMAIN_NAME')
api_key = os.getenv('API_KEY')
GameDatabase().upsert_game_entry(client_id)  # 引数がないときは売れ筋ゲームを取る
GameDatabase().upsert_app_details()
GameDatabase().upsert_achievements(steam_id=client_id)
GameDatabase().upsert_tags()
