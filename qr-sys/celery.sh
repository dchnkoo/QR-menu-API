#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=app.framework.celery.object:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.framework.celery.object:celery flower
fi