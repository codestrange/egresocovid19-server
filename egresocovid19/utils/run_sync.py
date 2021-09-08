import asyncio


def run_sync(arg):
    return asyncio.get_event_loop().run_until_complete(arg)
