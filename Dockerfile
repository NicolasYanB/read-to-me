FROM python:3.9.19-bookworm
WORKDIR /app

RUN apt-get update && \
  apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --timeout=45

COPY ./download_model.sh .
RUN ./download_model.sh

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
