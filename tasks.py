from celery import Celery
from celery.schedules import crontab
import scraper  


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/0'

celery_app = Celery('tasks',
                    broker=BROKER_URL,
                    backend=BACKEND_URL)

celery_app.conf.beat_schedule = {
    
    'run-scraper-every-30-minutes': {
        'task': 'tasks.run_main_scraper',
        
        'schedule': crontab(minute='*/30'),
    },
}
celery_app.conf.timezone = 'UTC'


@celery_app.task(name='tasks.run_main_scraper')
def run_main_scraper():
    """
    This is the Celery Task.
    When triggered by the scheduler (Beat), it calls the main scraper function.
    """
    try:
        print(f"CELERY TASK: Starting scraper.run_scraper()...")
        scraper.run_scraper()
        print(f"CELERY TASK: scraper.run_scraper() finished.")
        return "Scraping completed successfully."
    except Exception as e:
        print(f"CELERY TASK: Error running scraper: {e}")
        return f"Scraping failed: {e}"