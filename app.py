import os
from flask import Flask, jsonify, request, abort

from flask_cors import CORS
from auth import requires_auth, AuthError
from models import setup_db, db_drop_and_create_all, Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        return "Hello"

    """
    Movie endpoints
    """
    @app.route('/movies', methods=['GET'])
    def get_movies():
        """
        Get all movies endpoint
        """
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies/<movie_id>', methods=['GET'])
    @requires_auth('get:movies-detail')
    def get_movie_details(payload, movie_id):
        """
        Get specific movie details endpoint
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        """
        Create movie endpoint
        """
        body = request.get_json()

        for field in ['title', 'release_date', 'actor_id']:
            if field not in body:
                abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actor_id = body.get('actor_id', None)

        try:
            movie = Movie(title=title, release_date=release_date)
            if actor_id:
                movie.actor_id = actor_id
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            })

        except Exception:
            abort(422)

    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, movie_id):
        """
        Update movie endpoint
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        # Throw an error if no movie is found
        if not movie:
            abort(404)

        # Get body data
        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title', movie.title)
        release_date = body.get('release_date', movie.release_date)
        actor_id = body.get('actor_id', movie.actor_id)

        try:
            # Update actor
            movie.title = title
            movie.release_date = release_date
            movie.actor_id = actor_id
            movie.update()

            # Return movie data
            return jsonify({
                'success': True,
                'movie': [movie.format()],
            })
        except Exception:
            abort(422)

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        """
        Delete movie endpoint
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            })
        except:
            abort(422)

    """
    Actor endpoints
    """

    @app.route('/actors', methods=['GET'])
    def get_actor():
        """
        Get all actors endpoint
        """
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<actor_id>', methods=['GET'])
    @requires_auth('get:actors-detail')
    def get_actor_details(payload, actor_id):
        """
        Get Actor details endpoint
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        """
        Create actor endpoint
        """
        body = request.get_json()

        for field in ['name', 'gender', 'age']:
            if field not in body:
                abort(400)

        name = body.get('name', None)
        gender = body.get('gender', None)
        age = body.get('age', None)

        try:
            actor = Actor(name=name, gender=gender, age=age)
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format(),
            })

        except Exception:
            abort(422)

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, actor_id):
        """
        Update actor endpoint
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        # Throw an error if no actor is found
        if not actor:
            abort(404)

        # Get body data
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', actor.name)
        gender = body.get('gender', actor.gender)
        age = body.get('age', actor.age)

        try:
            # Update actor
            actor.name = name
            actor.gender = gender
            actor.age = age
            actor.update()

            # Return actors data
            return jsonify({
                'success': True,
                'actor': actor.format(),
            })
        except Exception:
            abort(422)

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        """
        Delete actor endpoint
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            })
        except:
            abort(422)

    """
    Error handlers
    """

    @app.errorhandler(400)
    def invalid(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def AuthErrorHandler(error):
        return jsonify({
            "success": False,
            "error": error.error['code'],
            "message": error.error['description']
        }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run()