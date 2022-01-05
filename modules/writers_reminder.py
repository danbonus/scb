import asyncio, datetime
import aioschedule
from repositories.grades import GradesRepository
from repositories.many_users import ManyUsersRepository
from datetime import datetime, timedelta
from utils.api import Api
from random import randint


async def remind_writers(schedule: aioschedule):
    print('beu')
    grades: GradesRepository = await GradesRepository()
    for grade in await grades.list:
        for bell, bell_data in grade.bells.items():
            time_to_remind = datetime.strptime(bell_data.end, "%H:%M") + timedelta(minutes=10)
            schedule.every().day.at(time_to_remind.strftime("%H:%M")).do(remind)


async def remind():
    if datetime.now().weekday() != 6:
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
