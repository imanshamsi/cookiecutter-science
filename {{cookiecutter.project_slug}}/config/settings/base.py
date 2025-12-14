import os
from config.env import  get_env, BASE_DIR
# Set application domain name
APP_DOMAIN = get_env(key='APP_DOMAIN', default='{{ cookiecutter.project_slug }}')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", True)

# Database
DATABASES = {
    'default': get_env(
        'DEFAULT_DB_URL', default="sqlite:///example.db"
    ),
    # Add more data sources here ...
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

# Logs folder
LOG_DIR = BASE_DIR / 'logs'

# {% if cookiecutter.use_celery == "y" %}
# from config.celery import *
# {% endif %}
