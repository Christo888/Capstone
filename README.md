# Capstone

### Motivation
Things I learned in this course:
1) Creating flask apps
2) Flask APIs
3) Authentication with jwt and auth0
4) Deployment with AWS/Heroku

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend using a virtual environment to keep your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Running the server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
```

To run the server, execute:

```bash
flask run --reload
```

### Auth0 roles

#### Casting director:
-Can view actors and movies  
-Add or delete an actor from the database

#### Casting assistant:
-Can view actors and movies  
-Add or delete an actor from the database  
-Modify actors or movies

#### Executive producer:
-Can view actors and movies  
-Modify actors or movies  
-Add or delete an actor from the database  
-Add or delete a movie from the database  


#### Site Base URL:
https://capstone-hero.herokuapp.com/

## Endpoints

### Movie Endpoints
#### GET Movies : /movies
#### GET Movie detail : /movies/<movie_id>
#### POST Movie : /movies
#### PATCH Movie : /movies/<movie_id>
#### DELETE Movie : /movies/<movie_id>

### Actor Endpoints
#### GET Actors : /actors
#### GET Actor detail : /actors/<movie_id>
#### POST Actor : /actors
#### PATCH Actor : /actors/<movie_id>
#### DELETE Actor : /actors/<movie_id>
