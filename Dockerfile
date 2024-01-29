FROM python:3.10.12

WORKDIR /qr-system

COPY . /qr-system

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN alembic revision --autogenerate

RUN alembic upgrade head

CMD [ "uvicorn", "app.API.api:app", "--host", "0.0.0.0", "--port", "8080" ]