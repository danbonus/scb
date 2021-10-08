from . import UserBlockedMiddleware, LogMiddleware


middlewares = [
    UserBlockedMiddleware.UserBlockedMiddleware(),
    LogMiddleware.LogMiddleware()
]
