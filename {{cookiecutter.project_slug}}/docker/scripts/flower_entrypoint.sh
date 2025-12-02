#!/bin/sh

set -e

# create new worker
echo "--> Starting flower web server ..."
celery -A {{ cookiecutter.project_slug }}.setup flower
