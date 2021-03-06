FROM python:3.10-slim as venvbuild

ENV PATH="/venv/bin:$PATH"
COPY requirements.txt ./
RUN python3 -m venv /venv && pip3 install -r requirements.txt

FROM python:3.10-slim as venvtest
RUN apt update && apt install -y libmagic1
# "Why, oh why, can't COPY just work like cp??" - colincameron
COPY --from=venvbuild /venv /work/venv
COPY ./app /work/app
WORKDIR /work/app 

ENV PATH="/work/venv/bin:$PATH"
ENV CONFIG_PATH="configs/test_config.py"
RUN python3 test.py

FROM python:3.10-alpine as venvrun
COPY --from=venvtest /work /
WORKDIR /app

RUN apk add libmagic curl
ENV PATH="/venv/bin:$PATH"
ENV CONFIG_PATH="configs/prod_config.py"
EXPOSE 8000
HEALTHCHECK --interval=3s --timeout=3s CMD curl --fail http://localhost:8000/health || exit 1
ENTRYPOINT ["gunicorn", "yesntga:app"]
# If shit goes wrong, uncomment the line below:
#ENTRYPOINT [ "tail", "-f", "/dev/null" ]