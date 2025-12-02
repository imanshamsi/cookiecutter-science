#!/bin/sh

set -e

# create new worker
echo "--> Creating new worker ..."
celery -A {{ cookiecutter.project_slug }} worker --loglevel=INFO
