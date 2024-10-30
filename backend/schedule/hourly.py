import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.hsms_vip import VipProductSearchService

hourlyScheduler = AsyncIOScheduler()


async def fetch_vip_product_data():
    print("Fetching VIP product data")
    svc = VipProductSearchService()
    data = await svc.fetch_vip_product_images()
    svc.extract_vip_product_features()
    print("VIP product data fetched and processed")

@hourlyScheduler.scheduled_job('interval', minutes=60*12)
async def common_scheduler_2hrs():
    print("Starting common scheduler job")
    await fetch_vip_product_data()

    print("Common scheduler job completed")

next_run_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
hourlyScheduler.add_job(common_scheduler_2hrs, 'date', run_date=next_run_time)