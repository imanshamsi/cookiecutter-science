from config.utils.celery import taskify


@taskify
def task1():
    """
    Task description placed here ...
    """
    print('task1 executed ...')
