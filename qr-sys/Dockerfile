FROM python:3.10.12

WORKDIR /qr-system

COPY . /qr-system

RUN chmod +x ./app.sh

RUN pip install --upgrade pip

RUN pip install -r requirements.txt