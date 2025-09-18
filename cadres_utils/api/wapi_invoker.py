import aiohttp

from cadres_utils.api.exception import ApiException, ApiUnauthorizedException


class WapiInvoker:
    def __init__(self, host: str, auth_token: str | None, jwt_token: str | None = None):
        self.__auth_token = auth_token
        self.__jwt_token = jwt_token
        self.__host = host
        if not auth_token and not jwt_token:
            raise ApiException('WapiInvoker init error. No auth token provided')

    async def post_request(self, object_operation, request_body) -> dict:
        url = self.get_wapi_base_url() + object_operation

        headers = {
            "Content-Type": "application/json"
        }
        if self.__jwt_token:
            headers["Authorization"] = f"Bearer {self.__jwt_token}"
        if self.__auth_token:
            headers["Cookie"] = f"sid={self.__auth_token}"

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=request_body, ssl=False) as response:
                res = await response.json()
                if response.status != 200 or res['ResponseCode'] != '000':
                    if res['ResponseCode'] == '401':
                        raise ApiUnauthorizedException(f'Unauthorized. Operation: {object_operation}. Response: {res}')
                    raise ApiException(f'Request error. Operation: {object_operation}. Response: {res}')
        return res

    def get_wapi_base_url(self):
        protocol = '' if '://' in self.__host else 'https://'
        return f'{protocol}{self.__host}/wapi/'

    def get_cookies(self):
        return {'sid': self.__auth_token}
