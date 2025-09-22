import json
import time
from typing import Tuple

import aiohttp
import jwt
from jwt import PyJWK

from cadres_utils.api.exception import ApiException, ApiUnauthorizedException


class WapiInvoker:
    def __init__(self, host: str, auth_token: str):
        self.__auth_token = auth_token
        self.__host = host

    async def post_request(self, object_operation, request_body) -> dict:
        res, _ = await self.post_request_with_headers(object_operation, request_body)
        return res


    async def post_request_with_headers(self, object_operation, request_body) -> Tuple[dict, dict]:
        url = self.get_wapi_base_url() + object_operation

        headers = self._get_headers()

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=request_body, ssl=False) as response:
                res = await response.json()
                response_headers = dict(response.headers)
                if response.status != 200 or res['ResponseCode'] != '000':
                    if res['ResponseCode'] == '401':
                        raise ApiUnauthorizedException(f'Unauthorized. Operation: {object_operation}. Response: {res}')
                    raise ApiException(f'Request error. Operation: {object_operation}. Response: {res}')
        return res, response_headers


    def get_wapi_base_url(self):
        protocol = '' if '://' in self.__host else 'https://'
        return f'{protocol}{self.__host}/wapi/'

    def get_cookies(self):
        return {'sid': self.__auth_token}

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json"
        }
        if self.__auth_token:
            headers["Cookie"] = f"sid={self.__auth_token}"

        return headers


class JWTWapiInvoker(WapiInvoker):
    def __init__(self, host: str, jwk_private_key_path: str):
        super().__init__(host=host, auth_token='')
        self.__jwk_private_key_path = jwk_private_key_path
        self.__jwk_data = self.__load_jwk()
        self.__private_key = PyJWK(jwk_data=self.__jwk_data, algorithm='RS256')

    def _get_headers(self):
        headers = super()._get_headers()
        headers['Authorization'] = f'Bearer {self.__get_token()}'

        return headers

    def __load_jwk(self):
        with open(self.__jwk_private_key_path, 'r') as f:
            jwk_data = json.load(f)
        return jwk_data

    def __get_token(self) -> str:
        payload = {
            'sub': self.__jwk_data['sub'],
            'aud': self.__jwk_data['aud'],
            "iat": int(time.time()),
            "iss": self.__jwk_data['iss'],
        }
        print(payload)

        token = jwt.encode(payload, self.__private_key, algorithm="RS256")

        return token
