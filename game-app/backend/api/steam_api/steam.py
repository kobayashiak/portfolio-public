from dotenv import load_dotenv
import os
from api.steam_api.users import Users
from api.steam_api.client import Client
from api.steam_api.apps import Apps


class Steam:
    load_dotenv()

    def __init__(self, api_key: str):
        self._users = Users(client=Client(key=api_key))
        self._apps = Apps(client=Client(key=api_key))
        self._client_id = os.getenv('STEAM_ID')

    @property
    def users(self):
        return self._users

    @property
    def apps(self):
        return self._apps
