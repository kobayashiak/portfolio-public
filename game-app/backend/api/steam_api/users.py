
from api.steam_api.client import Client
from typing import TypedDict, List


class Games(TypedDict):
    appid: int
    name: str
    playtime_forever: int
    img_icon_url: str
    has_community_visible_stats: bool
    playtime_windows_forever: int
    playtime_mac_forever: int
    playtime_linux_forever: int
    playtime_deck_forever: int
    rtime_last_played: int
    playtime_disconnected: int


class OwnedGameResponse(TypedDict):
    game_count: int
    games: List[Games]


class OwendGameAchievement(TypedDict):
    pass


class Users:

    def __init__(self, client: Client):
        self.client = client

    def get_owned_games(self, steam_id, include_appinfo: bool = False, include_free_games: bool = False, language: str = "japanese") -> OwnedGameResponse:

        params = {
            "steamid": steam_id,
            "include_appinfo": include_appinfo,
            "include_played_free_games": include_free_games
        }

        raw_res = self.client.request(
            'get',
            "/IPlayerService/GetOwnedGames/v1/",
            params=params,)

        if isinstance(raw_res, dict) and "response" in raw_res:
            return raw_res['response']

        return {'game_count': 0, "games": []}

    def get_user_achievement(self, steam_id: str, app_id: str, l: str = 'japanese'):

        params = {
            'steamid': steam_id,
            'appid': app_id,
            'l': l
        }

        raw_res = self.client.request(
            'get', '/ISteamUserStats/GetPlayerAchievements/v0001/', params=params)

        return raw_res.get('playerstats').get('achievements')
