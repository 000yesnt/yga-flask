# yesnt.ga - flask backend
Docker image for my Flask app.
The website HTML code is at the html folder. Read and seethe.

# Setting up
This project uses Docker Compose. You need to set up secrets before composing; see [secrets/README.md](secrets/README.md)

The compose file creates three containers: **flask**, **db** and **nginx**. Their dockerfiles are located at [the docker folder.](docker/)

### Database (db)
* Alpine MariaDB
* Port 3366
* Has its own volume for database files

### App (flask)
* Python 3.10
* Shares the Depot volume with NGINX.

### Web (nginx)
* Latest NGINX Apine
* Shares the Depot volume with flask.
* Port 8086

This code does not include the blog, or any Depot users.

# Running

Make a venv from `requirements.txt`. I tested this app with Python 3.8 and the Docker image uses Python 3.10. Anything in that version bracket should work.

In the `/app` directory, assuming Bash is your command line, run:
`FLASK_APP=yesntga:app FLASK_ENV=development flask run`