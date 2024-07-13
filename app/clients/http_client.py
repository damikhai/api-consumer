from typing import Literal

import httpx

from .utils import retry_decorator


class HttpClient:
    @staticmethod
    @retry_decorator
    async def request(method: Literal["POST", "DELETE", "GET"], url: str, json=None):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=json)
            return response
