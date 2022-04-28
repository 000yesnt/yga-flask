FROM yobasystems/alpine-mariadb:latest
COPY ./schemas/ /docker-entrypoint-initdb.d/
