from . import UserBlockedMiddleware, LogMiddleware, EmulationMiddleware, DebugMiddleware


middlewares = [
    UserBlockedMiddleware.UserBlockedMiddleware(),
    LogMiddleware.LogMiddleware(),
    EmulationMiddleware.EmulationMiddleware(),
    DebugMiddleware.DebugMiddleware()
]
