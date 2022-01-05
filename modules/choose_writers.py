import asyncio, datetime
import aioschedule
from repositories.grades import GradesRepository
from repositories.many_users import ManyUsersRepository
from datetime import datetime, timedelta
from utils.api import Api
from random import randint


async def choose():
    grades: GradesRepository = await GradesRepository()
    writers = await ManyUsersRepository.get_writers()
    print('sex')
    print(writers)
    for i in await grades.list:
        print(i)
        for writer in writers:
            print(i)
            await Api.api.messages.send(user_id=writer.uid, message="нужно заполнить дз",
                                        random_id=randint(-2e10, 2e10))
