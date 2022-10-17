from apscheduler.schedulers.background import BackgroundScheduler
from .views import update_seller_offers


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_seller_offers, 'cron', hour='19')
    scheduler.start()
    
    