FROM python:3.10.12

RUN apt-get update && apt-get install -y \
    supervisor \
    && rm -rf /vat/lib/apt/lists/*

RUN mkdir -p /etc/supervisor/conf.d

COPY supervisord.conf /etc/supervisor/supervisord.conf

WORKDIR /qrsystem

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./*.sh

CMD [ "./app.sh" ]