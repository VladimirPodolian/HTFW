import httpx

from src.data_for_testing.general_data import BASE_URL


class ApiBuilder:
    def __init__(self, base_url=f'{BASE_URL}/ru/api/'):
        self.base_url = base_url

    def __getattr__(self, request_method):
        return lambda *args, **kwargs: self.request(request_method, *args, **kwargs)

    def request(self, method, url, **kwargs):
        return httpx.request(method, f'{self.base_url}{url}', **kwargs)