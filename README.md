# yesnt.ga - flask backend
Docker image for my Flask app. This is currently what my server is running, though it's not constantly up-to-date.
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
