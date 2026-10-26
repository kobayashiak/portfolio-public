import mysql.connector
from api.steam_api.steam import Steam
import os
from dotenv import load_dotenv
from models.games import GameDetailUpdate, Achievement, GameInfoFirst, GameTagId
from dataclasses import asdict
import time
import pprint
from utils.utils import get_tag_from_description, savelog, ensure_writable, connect_db
from google.api_core import exceptions
from utils.config import DB_CONFIG
from models.games import Description
import json


load_dotenv()
api_key = os.getenv('API_KEY')
app_status = os.getenv('APP_STATUS')

steam = Steam(api_key)


class GameDatabase:
    def _select_game_ids(self, condition: str, table: str):
        try:
            with connect_db() as (cur, conn):
                get_id_sql = f"SELECT DISTINCT games.id FROM {table} WHERE {condition};"
                cur.execute(get_id_sql)
                return [str(raw[0]) for raw in cur.fetchall()]
        except Exception as e:
            print('所持ゲームのidが取得できませんでした。')
            return []

    def get_game_detail(self, game_id):
        with connect_db() as (cur, conn):
            game_details_sql = "SELECT id,name,complete_rate,playtime,description,is_owned FROM games WHERE id=%s"
            achievement_sql = "SELECT a.id,a.api_name,a.display_name,a.percent,a.achieved,a.unlocktime,a.weight,a.description FROM achievements as a WHERE a.game_id=%s"
            tag_sql = "SELECT t.id,t.name,t.count FROM tags t LEFT OUTER JOIN game_tag_id as gti ON gti.tag_id=t.id WHERE gti.game_id = %s "
            cur.execute(game_details_sql, [game_id])
            game_detail = cur.fetchone()
            cur.execute(achievement_sql, [game_id])
            achievements = cur.fetchall()
            cur.execute(tag_sql, [game_id])
            tags = cur.fetchall()
            recommend_game_sql = "SELECT g.id,g.name,g.complete_rate,COUNT(gti1.tag_id) as count,g.is_owned FROM game_tag_id as gti1 JOIN game_tag_id as gti2 on gti1.tag_id = gti2.tag_id JOIN games as g ON gti2.game_id = g.id WHERE gti1.game_id = %s AND g.id != %s AND is_owned = 0 GROUP BY g.id ORDER BY count DESC LIMIT 5"
            cur.execute(recommend_game_sql, [game_id, game_id])
            recommend_games = cur.fetchall()
            return {'detail': game_detail, 'achievements': achievements, 'tags': tags, 'recommend_games': recommend_games}

    def get_games(self, offset: int, limit: int, freeword: str, order: bool, column: int):
        orders = "ASC" if order else "DESC"
        if column == 0:
            columns = "name"
        elif column == 1:
            columns = "complete_rate"
        else:
            columns = "name"

        search_word = f"%{freeword}%"

        with connect_db() as (cur, conn):
            base_sql = " FROM games as g LEFT OUTER JOIN game_tag_id as gti ON g.id = gti.game_id LEFT OUTER JOIN tags as t ON gti.tag_id = t.id WHERE (g.name LIKE %(1)s OR g.description LIKE %(2)s OR t.name LIKE %(3)s) AND is_owned = 1"
            get_games_sql = f"SELECT g.id,g.name,g.complete_rate,g.is_owned {base_sql} GROUP BY g.id ORDER BY " + \
                columns + " "+orders + \
                " LIMIT %(limit)s OFFSET %(offset)s"
            get_count_sql = f"SELECT count(DISTINCT g.id){base_sql}"
            cur.execute(get_games_sql, {
                "1": search_word, "2": search_word, "3": search_word, "limit": limit, "offset": offset})

            games_list = cur.fetchall()

            cur.execute(get_count_sql, {
                "1": search_word, "2": search_word, "3": search_word})
            total_count_row = cur.fetchone()
            total_count = total_count_row[0] if total_count_row else 0

            return {"items": games_list, "totalCount": total_count}

    def upsert_game_entry(self, steam_id: str = None):
        ensure_writable()

        sql_queue = "INSERT IGNORE INTO id_ai_queue(id) VALUES(%s)"
        sql_games = "INSERT INTO games(id,playtime,is_owned) VALUES(%(id)s,%(playtime)s,%(is_owned)s) ON DUPLICATE KEY UPDATE is_owned = GREATEST(is_owned,VALUES(is_owned)),playtime = GREATEST(playtime,VALUES(playtime));"

        if not steam_id:
            ids = steam.apps.get_specials_games() | steam.apps.get_topsellers_games()
            gameInfoFirsts = [GameInfoFirst.from_api(
                id, 0, 0) for id in ids]
        else:

            games = steam.users.get_owned_games(steam_id=steam_id)
            game_list = games.get('games', [])
            gameInfoFirsts = [GameInfoFirst.from_api(
                item['appid'], item['playtime_forever'], 1) for item in game_list]

        id_list = [(gameInfoFirst.id,) for gameInfoFirst in gameInfoFirsts]
        with connect_db() as (cur, conn):
            cur.executemany(
                sql_games, [asdict(ownGame) for ownGame in gameInfoFirsts])
            cur.executemany(sql_queue, id_list)
            conn.commit()
            print('games及びid_ai_queueに対してidのみの登録完了')

    def upsert_app_details(self):
        """
        upsert_app_details の Docstring

        :param self: ゲームの詳細情報を格納するメソッド
        """

        ensure_writable()

        with connect_db() as (cur, conn):
            id_list = self._select_game_ids(
                'games.name IS NULL', 'games')
            s = 1
            for id in id_list:
                res_app_details = steam.apps.get_app_details(  # このメソッドは、既にdata内部の値までもってきているので、ここで掘る必要はないよ
                    app_id=id)

                if res_app_details:
                    gameInfo = GameDetailUpdate.from_api(
                        res_app_details, int(id))

                    set_data_sql = "UPDATE games SET name = %(name)s, description = %(description)s  WHERE id = %(id)s"
                    cur.execute(set_data_sql, asdict(gameInfo))
                    conn.commit()
                    print(f'{s}件目のデータを更新しました。')
                    s += 1
                    time.sleep(1.5)  # APIの制限に引っかからないように
                else:
                    print(f'何らかの要因で、{s}件目のデータ更新が失敗しました。')
                    pprint.pprint(res_app_details)
                    s += 1
                    time.sleep(1.5)  # 同上

    def upsert_achievements(self,  steam_id: str):

        ensure_writable()

        id_list = self._select_game_ids(
            'games.is_owned = 1', 'games LEFT JOIN achievements ON games.id = achievements.game_id ')

        for id in id_list:
            try:
                with connect_db() as (cur, conn):
                    print(f"ID:{id} の実績と進捗率")

                    res_global = steam.apps.get_app_achievement(app_id=id)
                    if not res_global:
                        print('実績ないよ！')
                        continue
                    res_global_achievement_map = {a['name']: a['percent']
                                                  for a in res_global}

                    res_user_achievement = steam.users.get_user_achievement(
                        steam_id, app_id=id)

                    achievement_list: list[Achievement] = []
                    total_weight = 0.0
                    user_weight = 0.0

                    for user_achi in res_user_achievement:
                        apiname = user_achi.get('apiname')

                        percent = float(
                            res_global_achievement_map.get(apiname, 0.0))

                        raw_weight = 100 / (percent+1)

                        if 20 <= percent <= 40:
                            final_weight = raw_weight * 1.5
                        elif percent <= 1:
                            final_weight = 1.0
                        else:
                            final_weight = raw_weight

                        obj = Achievement(game_id=id,
                                          api_name=apiname,
                                          display_name=user_achi.get(
                                              'name'),
                                          percent=percent,
                                          achieved=user_achi.get(
                                              'achieved'),
                                          description=user_achi.get(
                                              'description'),
                                          unlocktime=user_achi.get(
                                              'unlocktime'),
                                          weight=round(final_weight, 2))

                        achievement_list.append(obj)
                        total_weight += final_weight
                        user_weight += final_weight if user_achi.get(
                            'achieved') == 1 else 0.0

                    complete_rate = round(
                        user_weight/total_weight * 100, 2) if total_weight > 0 else 0.0
                    achievement_sql = "INSERT INTO achievements(game_id,api_name,display_name,percent,achieved,unlocktime,weight,description) VALUES(%(game_id)s,%(api_name)s,%(display_name)s,%(percent)s,%(achieved)s,%(unlocktime)s,%(weight)s,%(description)s) ON DUPLICATE KEY UPDATE achieved = VALUES(achieved), unlocktime = VALUES(unlocktime), percent = VALUES(percent)"
                    rate_sql = 'UPDATE games SET complete_rate=%(complete_rate)s where id = %(id)s'

                    cur.executemany(achievement_sql, [asdict(
                        achievement) for achievement in achievement_list])
                    cur.execute(
                        rate_sql, {'complete_rate': complete_rate, 'id': id})
                    conn.commit()
                    print(f"ID:{id} の実績と進捗率({complete_rate}%)を保存しました。")
                    time.sleep(1.5)
            except Exception as e:
                print(f'実績情報の格納に失敗しました。:{e}')
                continue

    def upsert_tags(self):
        ensure_writable()

        with connect_db() as (cur, conn):
            get_description_sql = "SELECT games.id,games.description FROM games INNER JOIN id_ai_queue ON games.id=id_ai_queue.id WHERE status = 0 "
            cur.execute(get_description_sql)
            chunk_size = 5
            descriptions = [Description(
                id=description[0], description=description[1]) for description in cur.fetchall()]
            targetChunks = [descriptions[i:i+5]
                            for i in range(0, len(descriptions), chunk_size)]

            for targetChunk in targetChunks:
                try:
                    tag_dict_chunks = get_tag_from_description(
                        targetChunk)
                    savelog("output.txt", json.dumps(
                        tag_dict_chunks, ensure_ascii=False, indent=2))
                    for tag_dict in tag_dict_chunks:

                        tags = tag_dict["tags"]
                        if len(tags) == 0:
                            continue
                        tag_set_sql = 'INSERT INTO tags(name,count) VALUES(%s,1) ON DUPLICATE KEY UPDATE count = count+1 '
                        cur.executemany(
                            tag_set_sql, [(tag,) for tag in tags])
                        placeholders = ','.join(['%s'] * len(tags))
                        tag_get_sql = f'SELECT id FROM tags WHERE name IN ({placeholders}) '
                        cur.execute(
                            tag_get_sql, tuple(tags))
                        tag_id_list = [GameTagId(
                            game_id=tag_dict["id"], tag_id=tag_id[0]) for tag_id in cur.fetchall()]
                        tag_game_set_sql = 'INSERT IGNORE INTO game_tag_id(game_id,tag_id) VALUES(%(game_id)s,%(tag_id)s)'
                        cur.executemany(tag_game_set_sql, [asdict(
                            tag_id) for tag_id in tag_id_list])
                        cur.execute(
                            'UPDATE id_ai_queue SET status = 1 WHERE id = %s', (tag_dict["id"],))
                        conn.commit()

                except exceptions.ResourceExhausted as e:
                    print(f'本日のAPI制限が来ました。:{e}')
                    break
                except Exception as e:
                    print(f'制限以外のエラー、次のタグ抽出を行います。:{e}')
                    continue
                finally:
                    time.sleep(20)
