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

To run the server run the following:

```bash
source env_bash.sh
```

Or each time you open a new terminal session, run:

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
```
Request Data: None   
Return Data: {  
    'movies': [{'id': 8, 'release_date': 'Tue, 31 Dec 2019 22:00:00 GMT', 'title': 'Test Movie Create'},],
    'success': True  
} 
``` 
#### POST Movie : /movies
```
Request Data: {
    'title': 'Test Movie Create', 
    'release_date': '2020-01-01', 
    'actor_id': '20'
} 
Return Data: {
    'movie': {'id': 8, 'release_date': 'Tue, 31 Dec 2019 22:00:00 GMT', 'title': 'Test Movie Create'}, 
    'success': True
}
```
#### PATCH Movie : /movies/<movie_id>
```
Request Data: {
    'title': 'Update Movie'
} 
Return Data: {
    'movie': [{'id': 15, 'release_date': 'Sun, 06 Jun 2021 22:00:00 GMT', 'title': 'Update Movie'}], 
    'success': True
}
```
#### DELETE Movie : /movies/<movie_id>
```
Request Data: {'id': '20'} 
Return Data: {
    'delete': '20', 
    'success': True
}
```
### Actor Endpoints
#### GET Actors : /actors
```
Request Data: None
Return Data: {
    'actors': [{'age': 25, 'gender': 'Male', 'id': 27, 'name': 'Test Actor'},], 
    'success': True
}
```
#### POST Actor : /actors
```
Request Data: {
'name': 'Test Actor',
    'gender': 'Male',
    'age': 25
} 
Return Data: {
    'actor': {'age': 25, 'gender': 'Male', 'id': 27, 'name': 'Test Actor'},
    'success': True
}
```
#### PATCH Actor : /actors/<movie_id>
```
Request Data: {
    'name': 'Update Actor'
} 
Return Data: {
    'actor': {'age': 25, 'gender': 'male', 'id': 10, 'name': 'Update Actor'},
    'success': True
}
```
#### DELETE Actor : /actors/<movie_id>
```
Request Data: {
    'id': '20'
} 
Return Data: {
    'delete': '20', 
    'success': True
}
```
## Running tests:
```bash
python test_app.py
```