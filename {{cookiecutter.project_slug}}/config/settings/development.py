from .base import *
from config.env import get_env

DEBUG = get_env("DEBUG", default=True, required=False)

# Logging for development
LOG_LEVEL = 'DEBUG'
LOG_FILE = LOG_DIR / 'dev.log'

# {% if cookiecutter.use_celery == "y" %}
# broker_url = 'memory://'
# result_backend = 'cache+memory://'

# task_always_eager = True
# task_eager_propagates = True
# {% endif %}
