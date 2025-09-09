import aiohttp

from cadres_utils.api.exception import ApiException, ApiUnauthorizedException


class WapiInvoker:
    def __init__(self, host: str, auth_token: str):
        self.__auth_token = auth_token
        self.__host = host

    async def post_request(self, object_operation, request_body) -> dict:
        url = self.get_wapi_base_url() + object_operation

        async with aiohttp.ClientSession(cookies=self.get_cookies()) as session:
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
