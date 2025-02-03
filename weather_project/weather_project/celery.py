"""from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')

app = Celery('weather_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')"""


from celery import Celery
import os

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')

app = Celery('weather_project')