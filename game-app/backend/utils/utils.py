from urllib.parse import urlencode
from typing import Optional, Union
import json
import re
from google import generativeai as genai
import os
from dotenv import load_dotenv
import re
from google.api_core import exceptions
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import time
from models.games import Description
from utils.config import DB_CONFIG
import mysql.connector
from contextlib import contextmanager
load_dotenv()


@contextmanager
def connect_db():
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                yield cur, conn
    except mysql.connector.Error as e:
        print(f'DBに接続できませんでした。:{e}')
        raise


def clean_dict(headers: dict = None):
    result = {}
    if not headers:
        return result

    for key, value in headers.items():
        match value:
            case None:
                continue
            case list():
                result[key] = ','.join(value)
            case bool():
                result[key] = 'true' if value else 'false'
            case _:
                result[key] = str(value)

    return result


def merge_dict(headers1: dict = None, headers2: dict = None):
    return clean_dict(headers1) | clean_dict(headers2)


def retry(times: int = 0, exceptions: tuple[type[Exception], ...] | None = None):

    if exceptions is None:
        exceptions = (Exception,)

    def decorator(func):
        def newfunc(*args, **kwargs):
            attempt = 1
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        f'{func.__name__}メソッドの{attempt}/{times}回目の試行で、{exceptions}のエラーが出ました。')
                    attempt += 1
            return func(*args, **kwargs)
        return newfunc

    return decorator


def build_with_map_params(url: str,  params: dict, key: Optional[str] = ''):

    encoded = urlencode(clean_dict(params))
    result = f'{url}?key={key}' if key else url
    sep = '&'if '?' in result else '?'

    return f'{result}{sep}{encoded}' if encoded else result


def get_tags(raw_text: str) -> list[dict]:
    candidates = [raw_text.strip()]
    match = re.search(r'\[.*\]', raw_text, re.DOTALL)
    if match:
        candidates.append(match.group(0))

    for tags_dict in candidates:
        try:
            return json.loads(tags_dict)
        except json.JSONDecodeError:
            continue
    print(f'解析失敗:{raw_text}')
    return []


def get_tag_from_description(descriptions: list[Description]) -> Union[list[dict] | Exception]:

    description = "\n\n".join(
        f"---ID:{item.id}---\n内容: {item.description}" for item in descriptions)
    savelog("input.txt", description)
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    tags: list[dict] = []
    if not description or len(description.strip()) < 5:
        return generateErrorTags(
            errorText="タグ無し", descriptions=descriptions)

    safety_settings = {HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                       HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                       HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                       HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }

    prompt = f"""
        あなたはゲーム分析とデータ分類のスペシャリストです。
        提示する5つのゲーム紹介文から、特徴を表すキーワードを各ゲーム最大10個抽出してください。

        【抽出ルール】
        - 紹介文が日本語以外なら翻訳して分析すること。
        - 「ジャンル・システム」と「世界観・固有名詞」をバランスよく含めること。
        - 表記ゆれを抑え、検索に強い一般的な名称に統一すること。

        【出力形式（厳守）】
        以下のJSON配列形式のみを出力してください。余計な解説文は一切不要です。
        [
         {{"id": ゲームID, "tags": ["タグ1", "タグ2", "タグ3"]}},
        ...
        ]

        【分析対象】
        {description}
        """

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(
        'models/gemini-flash-latest', safety_settings=safety_settings)

    max_retries = 3

    for attempt in range(max_retries):
        try:
            res = model.generate_content(prompt, generation_config={
                                         "response_mime_type": "application/json"},
                                         request_options={"timeout": 10})
            savelog("output_by_AI.txt", res.text)

            if res.candidates and res.candidates[0].finish_reason == 3:
                print(f'安全フィルターでブロックされたよ')
                return generateErrorTags(
                    errorText="フィルターによる制限", descriptions=descriptions)
            tags = get_tags(res.text)
            print(f"【タグの中身】: {tags}")
            return tags
        except exceptions.ResourceExhausted as e:
            wait_time = (attempt+1)*10
            if attempt == max_retries-1:
                raise e
            else:
                print(f'一時的な制限:{wait_time}秒待機してリトライします。')
                time.sleep(wait_time)

        except exceptions.ServiceUnavailable as e:
            print('サーバーが不安定なので、５秒後にリトライ。')
            time.sleep(5)

        except Exception as e:
            print(f'skip不可避のエラー:{e}')
            return generateErrorTags(
                errorText='エラーによる抽出不可', descriptions=descriptions)


def savelog(filename: str, content: str):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("="*50+"\n")
        f.write(content+"\n")


def generateErrorTags(errorText: str, descriptions: list[Description]):

    return [{"id": item.id, "tags": [errorText]} for item in descriptions]


def extract_ids_recursively(data, founds_ids=None):
    if founds_ids is None:
        founds_ids = set()

    if isinstance(data, dict):
        if "items" in data and isinstance(data['items'], list):
            for item in data['items']:
                if isinstance(item, dict) and 'id' in item:
                    founds_ids.add(item["id"])

        for value in data.values():
            extract_ids_recursively(value, founds_ids)

    elif isinstance(data, list):
        for element in data:
            extract_ids_recursively(element, founds_ids)

    return founds_ids


def ensure_writable():
    if (os.getenv('APP_STATUS') == 'DEMO'):
        raise RuntimeError("DEMO版につきこの操作は許可されていません")
