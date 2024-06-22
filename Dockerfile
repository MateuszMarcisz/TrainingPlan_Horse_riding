FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000