#!/bin/bash

sleep 10

alembic revision --autogenerate

alembic upgrade head

uvicorn app.API.api:app --host=0.0.0.0 --port=8080