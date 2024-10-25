FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



RUN python manage.py makemigrations vetbook
RUN python manage.py makemigrations questions
RUN python manage.py makemigrations vetbook


RUN python manage.py migrate users
RUN python manage.py migrate questions
RUN python manage.py migrate vetbook
RUN python manage.py migrate


CMD ["python", "manage.py", "runserver_plus", "--cert-file", "cert.crt"]
