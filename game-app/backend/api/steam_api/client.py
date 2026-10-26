
import json
from dotenv import load_dotenv
import os
import requests
from utils.utils import merge_dict, build_with_map_params, retry

load_dotenv()
BASE_URL = os.getenv("API_BASE_URL")


class Client:
    def __init__(self, key: str = "", headers: dict = None):
        self.key = key
        self._headers = merge_dict({
            "Content-Type": "application/json",
            "Accept": "application/json",
        }, headers or {})
        self.session = requests.Session()

    @retry(times=3)
    def request(self, method: str, url: str, data: any = None, params: dict = None, headers=None):

        if not data:
            data = {}

        if not params:
            params = {}

        if 'https:' not in url:
            requestUrl = build_with_map_params(
                f'{BASE_URL}{url}', params=params, key=self.key)
        else:
            requestUrl = build_with_map_params(
                url, params=params)
        requestHeaders = merge_dict(self._headers, headers)
        requestData = json.dumps(data) if data else ""
        result = self.session.request(
            method, requestUrl, timeout=10, data=requestData, headers=requestHeaders)

        return self.__validator(result)

    @staticmethod
    def __validator(result: requests.Response):
        try:
            body = result.json()

        except Exception:
            body = {}
        if isinstance(body, dict) and body.get("code", None) is not None:
            raise Exception(body.get("description"))
        elif result.status_code >= 400:
            raise Exception(
                f"{result.status_code},{result.reason},{result.text}")
        elif len(result.text) == 0:
            return "OK"
        else:
            return body
