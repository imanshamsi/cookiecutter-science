#!/bin/sh

set -e

# create celery scheduler
echo "--> Start beat scheduler ..."
celery -A {{ cookiecutter.project_slug }} beat --loglevel=debug
