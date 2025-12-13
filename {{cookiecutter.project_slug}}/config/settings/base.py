import os

from config.env import BASE_DIR, load_environment, get_env


# Load application environments from .env
load_environment(os.path.join(BASE_DIR, '.env.example'))

# Set application domain name
APP_DOMAIN = get_env(key='APP_DOMAIN', default='{{ cookiecutter.project_slug }}')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True")

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

# {% if cookiecutter.use_celery == "y" %}
# from config.celery import *
# {% endif %}
