from datetime import datetime

from utils.args_object import SCB
from blueprints.homework.homework import get_homework
from repositories.many_users import ManyUsersRepository
from datetime import datetime, timedelta


async def broadcast():
    users = await ManyUsersRepository.get_broadcast_subscribers()
    time_dict = {}
    print(users)
    for i in users:
        print("listing users: %s" % i)
        if i.broadcast_time in time_dict:
            time_dict[i.broadcast_time].append(i.uid)
        else:
            time_dict[i.broadcast_time] = [i.uid]

    print(time_dict)

    for time_since, uids in time_dict.items():
        print(time_since)
        time_since = datetime.strptime(time_since, "%H:%M")
        for uid in uids:
            scb = await SCB({"user_id": uid})
            weekday = str(datetime.now().weekday())
            if weekday in scb.schedule.schedule:
                last_lesson = scb.schedule.schedule[weekday][-1]
                time = datetime.strptime(scb.grades.bells[last_lesson.bell].end, "%H:%M") + timedelta(hours=time_since.hour, minutes=time_since.minute)
                print(scb.grades.bells[last_lesson.bell].end)
                print(time.strftime("%H:%M"))

                if time.strftime("%H:%M") == datetime.now().strftime("%H:%M"):
                    await get_homework(message=None, scb=scb)
