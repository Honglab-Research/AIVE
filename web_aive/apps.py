from django.apps import AppConfig
from django.conf import settings
import os

class WebAiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_aive'
    
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import scheduler
            run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
            if run_once is not None:
                return
            os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 
            
            scheduler.start()
