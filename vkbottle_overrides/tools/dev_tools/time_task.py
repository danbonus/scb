from asyncio import sleep

from typing import Any, Callable, Coroutine

Handler = Callable[..., Coroutine[Any, Any, Any]]


class TimeTask:
    def __init__(self, time: int, handler: Handler, do_break: bool = False):
        self.time = time
        self.handler = handler
        self.do_break = do_break

    async def __call__(self, *args, **kwargs):
        while True:
            #print("sleeping for %s" % self.seconds)
            await sleep(self.seconds)
            await self.handler(*args, **kwargs)
            if self.do_break:
                break
