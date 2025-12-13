from .base import *

DEBUG = True

{% if cookiecutter.use_celery == "y" %}
broker_url = 'memory://'
result_backend = 'cache+memory://'

task_always_eager = True
task_eager_propagates = True
{% endif %}
