from asyncio import sleep

from typing import Any, Callable, Coroutine

Handler = Callable[..., Coroutine[Any, Any, Any]]


class DelayedTask:
    def __init__(self, seconds: int, handler: Handler, do_break: bool = False):
        self.seconds = seconds
        self.handler = handler
        self.do_break = do_break

    async def __call__(self, *args, **kwargs):
        while True:
            #print("sleeping for %s" % self.seconds)
            await sleep(self.seconds)
            await self.handler(*args, **kwargs)
            if self.do_break:
                break
