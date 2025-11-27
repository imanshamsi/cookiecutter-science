from celery import Celery

from config import settings
from config.utils.celery import register_tasks


# Create Celery app using project domain as the app name
app = Celery(settings.APP_DOMAIN)

# Apply Celery configuration from config.settings (broker, backend, etc.)
app.config_from_object(settings)

# Explicitly import task modules listed in config.celery
register_tasks(settings.TASK_APPS)
