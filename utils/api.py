#from vkbottle_overrides.bot import Blueprint
from vkbottle import API
from vkbottle import vkscript


#bp = Blueprint()

# костыль для простого доступа к апи у сторонних модулей


@vkscript
def cases(uid, cases_):
    requests = []

    for i in cases_:
        requests.append(api.users.get(user_ids=uid, name_case=i))  # это не обращение к локальной переменной,
        # а код для VkExecute. пусть горит красным, вообще похуй

    return requests


class Api:
    api: API
    user_api: API
    group_id: int

    def __init__(self, api=None):
        #self.group_id = CtxStorage().get("group_id")
        if api:
            self.api = api
        #self.group_id = self.get_group_id()

    async def get_group_id(self):
        return (await self.api.groups.get_by_id())[0].id

    @staticmethod
    @vkscript
    def cases(uid, cases_):
        requests = []

        for i in cases_:
            requests.append(api.users.get(user_ids=uid, name_case=i))  # это не обращение к локальной переменной,
            # а код для VkExecute. пусть горит красным, вообще похуй

        return requests

    @classmethod
    async def get_cases(cls, uid) -> dict:
        cases_dict = {}
        cases_list = ["nom", 'gen', 'dat', 'acc', 'ins', 'abl']

        code = cases(uid=uid, cases_=cases_list)
        result = (await cls.api.execute(code=code))["response"][::-1]
        print(result)
        for index, i in enumerate(result):
            i = i[0]
            cases_dict[cases_list[index]] = {
                "first_name": i["first_name"],
                "last_name": i["last_name"],
                "full_name": "%s %s" % (i["first_name"], i["last_name"])
            }

        return cases_dict

    @classmethod
    async def create_album(cls, label):
        albums = await cls.user_api.photos.get_albums(owner_id=cls().group_id)

        for i in albums.items:
            if label == i.title.split()[-1]:
                return i.id

        album = await cls.user_api.photos.create_album(
            title="Материалы домашнего задания %s" % label,
            description="Материалы, прилагающиеся к домашним заданиям в %s классе. Кстати, зачем ты сюда заглянул?" % label,
            group_id=cls().group_id,
            upload_by_admins_only=True
        )

        return album.id

    @classmethod
    async def has_album(cls, album_id):
        albums = await cls.user_api.photos.get_albums(owner_id=-cls().group_id, album_ids=[int(album_id)])

        if albums.items:
            return albums.items[0]

#async def check_longpoll_settings():
 #   settings = bp.api.groups.get_long_poll_settings()
