FROM python:3.10-slim as venvbuild

RUN apt update && apt install -y libmagic1

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN pip3 install -r requirements.txt

FROM python:3.10-alpine as venvrun
COPY --from=venvbuild /venv /venv
COPY ./app /app
WORKDIR /app

RUN apk add libmagic
ENV PATH="/venv/bin:$PATH"

EXPOSE 8000
ENTRYPOINT ["gunicorn", "wsgi:app"]
