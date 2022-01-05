from utils.api import Api


async def user(uid):
    user_model = {
        "uid": uid,
        "grade": None,
        "lang_group": None,
        "exam_group": None,
        "lang": "russian",
        "roles":
            {
                "writer": False,
                "admin": False,
                "blocked": False
            },
        "name_cases": await Api.get_cases(uid),
        "broadcast_user": False,
        "broadcast_time": None
    }

    return user_model
