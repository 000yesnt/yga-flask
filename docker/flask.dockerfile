FROM python:3.10-slim as venvbuild

ENV PATH="/venv/bin:$PATH"
COPY ./app/test_config.py requirements.txt ./
RUN apt update && apt install -y libmagic1
RUN python3 -m venv /venv && pip3 install -r requirements.txt


FROM python:3.10-alpine as venvrun
COPY --from=venvbuild /venv /venv
COPY ./app /app
WORKDIR /app

RUN apk add libmagic
ENV PATH="/venv/bin:$PATH"
ENV CONFIG_PATH="../prod_config.py"
EXPOSE 8000
ENTRYPOINT ["gunicorn", "yesntga:app"]
