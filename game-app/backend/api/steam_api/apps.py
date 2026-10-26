from api.steam_api.client import Client

from typing import TypedDict, Optional, List

from dotenv import load_dotenv
from utils.utils import savelog, extract_ids_recursively
import json
import os
import time
import re


load_dotenv()
API_APP_DETAILS_URL = os.getenv('API_APP_DETAILS_URL')
API_GET_TOP_URL = os.getenv('API_GET_TOP_URL')
API_APP_SEARCH_RESULT_URL = os.getenv('API_APP_SEARCH_RESULT_URL')


class GameInfo(TypedDict):
    name: str
    steam_appid: int
    required_age: int
    is_free: bool
    controller_support: Optional[str]
    dlc: Optional[List[int]]
    short_description: Optional[str]


class Apps:

    def __init__(self, client: Client):
        self.client = client

    def get_app_details(self, app_id: str, l: str = 'japanese', filters: Optional[str] = 'basic', cc: str = 'JP') -> Optional[GameInfo]:
        params = {'appids': app_id,
                  'l': l,
                  'filters': filters,
                  'cc': cc}

        res = self.client.request(
            'get', API_APP_DETAILS_URL, params=params,)
        return res.get(str(app_id)).get('data')

    def get_app_achievement(self, app_id: str):
        params = {'gameid': app_id, }

        res = self.client.request(
            'get', '/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/', params=params)

        return res.get('achievementpercentages').get('achievements')

    def get_specials_games(self):
        time.sleep(1.0)

        res = self.client.request(method='get',
                                  url=API_GET_TOP_URL,)
        ids = extract_ids_recursively(res)
        return ids

    def get_topsellers_games(self):
        time.sleep(1.0)

        params = {
            'filter': 'topsellers',
            'json': 1,
            'count': 200,
            'start': 0,
            'query': '',
            'sort_by': '_ASC'
        }

        res = self.client.request(method='get',
                                  url=API_APP_SEARCH_RESULT_URL, params=params)
        items = res.get('items', [])
        ids = set()
        for item in items:
            if 'logo' in item:
                match = re.search(r'/apps/(\d+)/', item['logo'])
                if match:
                    ids.add(match.group(1))
        return ids
