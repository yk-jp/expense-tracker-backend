FROM python:3.8

ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY docker-entrypoint.sh .
RUN chmod +x ./docker-entrypoint.sh

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]