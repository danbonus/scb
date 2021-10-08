from utils.api import Api


async def user(uid):
    user_model = {
        "uid": uid,
        "grade": None,
        "lang": "normal",
        "is_writer": False,
        "is_admin": False,
        "registered": False,
        "name_cases": await Api.get_cases(uid),
        "blocked": False,
        "first_entry": True
    }

    return user_model
