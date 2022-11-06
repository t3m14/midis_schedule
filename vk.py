from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from vkbottle.bot import Message
from vkbottle.user import User
from vkbottle import PhotoMessageUploader
from portal import MidisSchedule
from config import midis_password, midis_login
TOKEN = "vk1.a.nl1Qw7OBimepepyQ8G5z2LdVx8xUtP84q9AH1lTUzER8xiMx9_SZUgbdzykfO3KvDkxAj-JB6cViV0aNjPkN2sOPvRQn3swJrphq3Xu8f7cGMFMeUi_oBIdLKiHSSuOBf_GKH_SBX5YCjWe3ReXeNRcXCPXsuYsyOMkn0GrPf5w5NH-kC53_yF__cYJaaUJ-YW4awNPEdYV6CsDGqWORiA"
bot = User(token=TOKEN)


@bot.on.message(text="!расписание")
async def hi_handler(message: Message):
    await send_schedule()
    photo_uploader = PhotoMessageUploader(bot.api)
    midis = MidisSchedule(login="EbQLdH", password="ZJxwT9")
    midis.get_today_table()
    photo = await photo_uploader.upload("./images/today.png")
    await message.answer("Расписание на сегодня", attachment=photo)
    midis.get_tommorow_table()
    photo = await photo_uploader.upload("./images/tomorrow.png")
    await message.answer("А это расписание на завтра", attachment=photo)


async def send_schedule():
    midis.get_today_table()
    midis.get_tommorow_table()
    photo_uploader = PhotoMessageUploader(bot.api)
    photo = await photo_uploader.upload("./images/today.png")
    await bot.api.messages.send(
        peer_id="2000000169",
        random_id=0,
        message="Расписание на сегодня",
        attachment=photo,
    )
    photo = await photo_uploader.upload("./images/tomorrow.png")
    await bot.api.messages.send(
        peer_id="2000000169",
        random_id=0,
        message="Расписание на завтра",
        attachment=photo,
    )


if __name__ == "__main__":
    midis = MidisSchedule(login=midis_login, password=midis_password)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_schedule, "cron", hour=6, minute="*")
    scheduler.start()
    bot.run_forever()
