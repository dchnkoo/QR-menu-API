#!/bin/bash

sleep 10

alembic revision --autogenerate

alembic upgrade head

gunicorn app.API.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080