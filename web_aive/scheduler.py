from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from web_aive.utils.af2_singleton import Af2Singleton
import logging

#logging.basicConfig(level=logging.ERROR)
logging.getLogger('django_apscheduler.jobstores').setLevel(logging.ERROR)
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    
    @scheduler.scheduled_job('interval', seconds=5, name = 'prdctn_job_check', id='predctn_job_check')
    def auto_check():
        af2_s = Af2Singleton()        
        af2_s.prdctn_job_check()
        
    scheduler.start()