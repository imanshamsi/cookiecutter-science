import importlib

from celery import shared_task


def taskify(func):
    return shared_task(name=func.__name__)(func)


def register_tasks(app_list):
    for app_name in app_list:
        try:
            importlib.import_module(app_name)
        except ImportError as e:
            raise ImportError(f"Failed to import app '{app_name}': {e}")
