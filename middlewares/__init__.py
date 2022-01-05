from . import ChatMiddleware, UserBlockedMiddleware, LogMiddleware, EmulationMiddleware, MaintenanceMiddleware, DebugMiddleware


middlewares = [
    ChatMiddleware.ChatMiddleware(),
    UserBlockedMiddleware.UserBlockedMiddleware(),
    LogMiddleware.LogMiddleware(),
    EmulationMiddleware.EmulationMiddleware(),
    #DebugMiddleware.DebugMiddleware(),
    MaintenanceMiddleware.MaintenanceMiddleware()
]
