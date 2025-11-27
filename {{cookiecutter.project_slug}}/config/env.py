import os
from pathlib import Path

from .exceptions import ImproperlyConfigured


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def load_environment(env_file_path: str):
    from dotenv import load_dotenv

    if not os.path.exists(env_file_path):
        raise ImproperlyConfigured(f".env file not found at: {env_file_path}")

    load_dotenv(
        dotenv_path=env_file_path, verbose=True, override=True
    )


def get_env(key: str, default=None, required=True):
    value = os.getenv(key, default)
    if required and value is None:
        raise ImproperlyConfigured("Missing required environment variable: {key}")
    return value


def env_to_enum(*, enum_cls, value):
    for x in enum_cls:
        if x.value == value:
            return x
    raise ImproperlyConfigured(f"Env value {repr(value)} could not be found in {enum_cls.__name__}")
