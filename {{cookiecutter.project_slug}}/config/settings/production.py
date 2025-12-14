from .base import *

DEBUG = get_env("DEBUG", default=False , required=False)

# Logging for production
LOG_LEVEL = 'INFO'
LOG_FILE = LOG_DIR / 'prod.log'