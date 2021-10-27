from utils.api import Api


async def user(uid):
    user_model = {
        "uid": uid,
        "grade": None,
        "lang": "russian",
        "roles":
            {
                "writer": False,
                "admin": False,
                "blocked": False
            },
        "name_cases": await Api.get_cases(uid),
        "broadcast_info":
            {
                "subscriber": False,
                "type": None,
                "time": None
            }
    }

    return user_model
