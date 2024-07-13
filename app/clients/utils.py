import asyncio
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import httpx
from loguru import logger

from config import Config

env = Config()

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")

STATUS_WHEN_RETRY = (
    httpx.codes.TOO_MANY_REQUESTS,
    httpx.codes.INTERNAL_SERVER_ERROR,
    httpx.codes.SERVICE_UNAVAILABLE
)


def retry_decorator(method: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
    """Decorator for sending requests with retry policy."""
    @wraps(method)
    async def wrapper(
            self,
            *args: F_Spec.args,
            **kwargs: F_Spec.kwargs
    ) -> F_Return:
        retry = env.RETRY_COUNT
        while retry:
            try:
                response = await method(self, *args, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as err:
                if err.response.status_code in STATUS_WHEN_RETRY:
                    retry -= 1
                    if retry:
                        await asyncio.sleep(env.WAIT_BETWEEN_RETRIES)
                        logger.info(f"Retrying... {env.RETRY_COUNT - retry}/{env.RETRY_COUNT}")
                    else:
                        logger.error(f"Failed after {env.RETRY_COUNT} retries")
                        raise
                else:
                    raise
            except Exception as err:
                logger.error(f"An error occurred: {err}")
                raise
    return wrapper
