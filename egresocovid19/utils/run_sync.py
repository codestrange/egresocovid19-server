import asyncio
from typing import Awaitable, TypeVar

T = TypeVar("T")


def run_sync(arg: Awaitable[T]) -> T:
    return asyncio.get_event_loop().run_until_complete(arg)
