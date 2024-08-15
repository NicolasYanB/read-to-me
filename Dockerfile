FROM python:3.12-slim-bullseye
WORKDIR /app

RUN apt-get update && \
  apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
