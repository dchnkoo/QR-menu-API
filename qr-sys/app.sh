#! /bin/bash

sleep 5

python3 -m app.SECRET_KEY.generate --set-secret

sleep 5

alembic revision --autogenerate

alembic upgrade head

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf