#!/bin/bash

sleep 10

alembic revision --autogenerate

alembic upgrade head

gunicorn app.API.api:app -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080