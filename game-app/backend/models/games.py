
from dataclasses import dataclass
from typing import NamedTuple


@dataclass  # 実際にゲームの詳細情報をDBに保存する際に使うクラス
class GameDetailUpdate:
    id: int = 0
    name: str = None
    description: str = None

    @classmethod
    def from_api(cls, res_for_api: dict, id: int):

        return cls(id=id,
                   name=res_for_api.get('name', 'Unknown'),
                   description=res_for_api.get(
                       'short_description', ''),
                   )


@dataclass  # 実際にゲームの実績情報を保存するためのクラス、DBのAchievementsテーブル側とid及びgame_id以外は一致
class Achievement:
    game_id: int = None
    api_name: str = None
    display_name: str = None
    percent: float = None
    achieved: int = 0
    unlocktime: int = None
    weight: float = 0.0
    description: str = None


@dataclass  # 実際の所持ゲーム情報保存用
class GameInfoFirst:
    id: int
    playtime: int
    is_owned: int

    @classmethod
    def from_api(cls, id: int, playtime: int, is_owned: int):
        return cls(id=id, playtime=playtime, is_owned=is_owned)


@dataclass
class GameTagId:
    game_id: int
    tag_id: int


@dataclass  # gamesテーブルの構造を表す、現時点で使用予定なし、ドキュメント用途
class GameRow:
    id: int = 0
    playtime: int = 0
    name: str = None
    description: str = None
    complete_rate: float = 0.0


class Description(NamedTuple):
    id: int
    description: str
