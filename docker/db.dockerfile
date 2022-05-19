FROM mariadb:latest
COPY ./schemas/ /docker-entrypoint-initdb.d/
