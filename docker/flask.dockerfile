FROM python:3.10-slim

COPY ./yesntga/ /app
COPY ./requirements.txt /app
COPY ./wsgi.py /app
WORKDIR /app

RUN apt update
RUN apt install -y libmagic-dev
RUN pip3 install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["gunicorn", "-w", "6", "-k", "gevent", "-b", "0.0.0.0", "wsgi:app", "--access-logfile=-", "--error-logfile=-"]
