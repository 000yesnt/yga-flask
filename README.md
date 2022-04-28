[![Test Flask app](https://github.com/000yesnt/yesntga-flask/actions/workflows/test.yml/badge.svg)](https://github.com/000yesnt/yesntga-flask/actions/workflows/test.yml) [![Deploy Flask app](https://github.com/000yesnt/yesntga-flask/actions/workflows/deploy.yml/badge.svg)](https://github.com/000yesnt/yesntga-flask/actions/workflows/deploy.yml)
# yesnt.ga - flask backend
Docker image for my Flask app. As of writing, this isn't what the server's running yet.
The website HTML code is at the html folder. Read and seethe.

I don't know how the FUCK docker works so if something goes wrong w/ docker-compose, scream about it in issues or make a PR.

# Setting up
This project uses Docker Compose. You need to set up secrets before composing; see [secrets/README.md](secrets/README.md)

The compose file creates three containers: **flask**, **db** and **nginx**. Their dockerfiles are located at [the docker folder.](docker/)

### Database (db)
* Alpine MariaDB
* Port 3366
* Has its own volume for database files

### App (flask)
* Python 3.10
* Shares the Depot and Lynx volumes with NGINX.

### Web (nginx)
* Latest NGINX Apine
* Shares the Depot and Lynx volumes with flask.
* Port 8086

This code does not include the blog, or any Depot users.

For the app, you'll need additional setup for some of the routes:
* [Lynx @ /lynx; LynxWebP @ /lynx/webp](docs/lynx.md)