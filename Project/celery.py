import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

app = Celery('Project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-best-weekly-posts': {
        'task': 'NewsPortal.tasks.send_best_weekly_posts',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}

#celery -A Project worker -P threads
#celery -A Project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler