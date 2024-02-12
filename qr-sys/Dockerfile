FROM python:3.10.12

WORKDIR /qr-system

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./*.sh

