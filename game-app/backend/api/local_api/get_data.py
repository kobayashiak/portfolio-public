from fastapi import FastAPI, Query, HTTPException
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import math
from db.game_database import GameDatabase
from pydantic import BaseModel
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://xxx.xyz",
                   "https://api.xxx.xyz", "http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization",
                   "X-CSRF-Token", "Access-Control-Allow-Origin"],
)


class GameResponse(BaseModel):
    id: int
    name: str
    complete_rate: float
    count: int | None = None
    is_owned: int

    class Config:
        from_attributes = True


class GameResponses(BaseModel):
    items: list[GameResponse]
    totalCount: int
    max_page: int


class Tag(BaseModel):
    id: int
    name: str
    count: int


class Achievement(BaseModel):
    id: int
    api_name: str
    display_name: str
    percent: float
    achieved: bool
    unlocktime: int
    weight: float
    description: str


class GameDetailResponse(BaseModel):
    game: GameResponse
    playtime: int
    description: str
    tags: list[Tag]
    achievements: list[Achievement]
    recommend_games: list[GameResponse]


class DataNotFoundException(Exception):
    def __init__(self, game_id=""):
        self.game_id = game_id
        super().__init__(game_id)

    def __str__(self):
        return (f'[{self.game_id}]がidのゲームは存在しません。')


@app.get("/games", response_model=GameResponses)
def get_game_data(page: Annotated[int, Query(ge=1)] = 1, freeword: str = "", order: bool = True, column: int = 0):
    limit = 25
    offset = (page-1)*limit
    gameDatabase = GameDatabase()
    rows = gameDatabase.get_games(
        limit=limit, offset=offset, freeword=freeword, order=order, column=column)
    items = rows["items"]
    totalCount = rows["totalCount"]

    return GameResponses(items=[GameResponse(id=item[0], name=item[1], complete_rate=item[2], is_owned=item[3])for item in items],
                         totalCount=totalCount, max_page=math.ceil(totalCount/25))


@app.get("/gameDetail/{game_id}", response_model=GameDetailResponse)
def get_game_detail(game_id: int):
    try:
        gameDatabase = GameDatabase()
        rows = gameDatabase.get_game_detail(game_id=game_id)
        detail = rows['detail']
        if detail is None:
                raise DataNotFoundException(game_id=game_id)
        achievements = rows['achievements']
        tags = rows['tags']
        recommend_games = rows['recommend_games']

        return GameDetailResponse(game=GameResponse(id=detail[0], name=detail[1], complete_rate=detail[2], is_owned=detail[5]),
                                  playtime=detail[3],
                                  description=detail[4],
                                  tags=[Tag(id=tag[0], name=tag[1], count=tag[2])
                                        for tag in tags],
                                  achievements=[Achievement(id=achievement[0], api_name=achievement[1], display_name=achievement[2], percent=achievement[3], achieved=True if achievement[4]
                                                            == 1 else False, unlocktime=achievement[5], weight=achievement[6], description=achievement[7]) for achievement in achievements],
                                  recommend_games=[GameResponse(id=recommend_game[0], name=recommend_game[1], complete_rate=recommend_game[2], count=recommend_game[3], is_owned=recommend_game[4])for recommend_game in recommend_games])

    except DataNotFoundException as e:
        print(e)
        raise HTTPException(status_code=404, detail="Game not found")
