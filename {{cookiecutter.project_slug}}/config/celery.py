from celery.schedules import crontab

from .env import get_env


# https://docs.celeryproject.org/en/stable/userguide/configuration.html

# Broker and backend configuration settings
broker_url = get_env('CELERY_BROKER_LOCATION', default="redis://localhost:6379/0")
result_backend = get_env('CELERY_RESULT_LOCATION', default='db+sqlite:///celery_results.sqlite3')
broker_connection_retry_on_startup = True

# Serialization and content configuration settings
accept_content = ['json']
result_accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'

# Task execution behavior configuration settings
task_acks_late = True
task_reject_on_worker_lost = True
task_send_task_events = True
task_track_started = True
task_send_sent_event = True

# Task delivery defaults configuration settings
task_default_exchange_type = 'direct'
task_default_delivery_mode = 'persistent'

# Task time limits
task_time_limit = 300
task_soft_time_limit = 270

# Worker configuration settings
worker_concurrency = 1
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1
worker_max_memory_per_child = 250000
worker_disable_rate_limits = False
worker_send_task_events = True

# Timezone and clock configuration settings
enable_utc = True
timezone = 'UTC'

# Explicit list of task modules for Celery to import in place of autodiscovery.
TASK_APPS = [
    '{{ cookiecutter.project_slug }}.tasks.example',
    # Add more tasks file here
]

# Schedule tasks using beat
beat_schedule = {
    'task1': {
        'task': 'task1',
        'schedule': crontab(hour=1, minute=0),
        'args': (),
        'options': {}
    },
    # Add more tasks here ...
}
