import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from test_config import bearer_tokens
from datetime import date


class CapstoneTest(unittest.TestCase):
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        actors = Actor.query.all()
        for actor in actors:
            actor.delete()
        movies = Movie.query.all()
        for movie in movies:
            movie.delete()
        pass

    """
    Test casting assistant can view actors and movies
    """
    def test_get_all_actors(self):
        token = bearer_tokens['casting_assistant']
        resp = self.client().get('/actors', headers={
            'Authorization': token}
        )
        data = resp.get_json()
        actors = Actor.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], [actor.format() for actor in actors])

    def test_get_all_movies(self):
        token = bearer_tokens['casting_assistant']
        resp = self.client().get('/movies', headers={
            'Authorization': token}
            )
        data = resp.get_json()
        movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], [movie.format() for movie in movies])

    """
    Test casting agent can create/delete actors and modify actors and movies
    """
    def test_post_actor(self):
        new_actor = {
            'name': 'Test Actor',
            'gender': 'Male',
            'age': 25,
        }
        resp = self.client().post('/actors', headers={
            'Authorization': bearer_tokens['casting_director']},
            json=new_actor
        )
        actor = Actor.query.filter(Actor.name == 'Test Actor').one_or_none()
        data = resp.get_json()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor.format())

        actor.delete()

    def test_patch_actor(self):
        actor = Actor(
            name='New Actor',
            gender='male',
            age=25,
        )
        actor.id = 10
        actor.insert()

        resp = self.client().patch('/actors/10', headers={
            'Authorization': bearer_tokens['casting_director']},
            json={'name': 'Update Actor'}
        )
        data = resp.get_json()

        actor = Actor.query.filter(Actor.id == 10).one_or_none()
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.name, 'Update Actor')

        actor.delete()

    def test_patch_movie(self):
        actor = Actor(
            name='Actor update',
            gender='Male',
            age=21
        )
        actor.id = 15
        actor.insert()
        movie = Movie(
            release_date=date.today(),
            title='Test Movie'
        )
        movie.actor = actor
        movie.id = 15
        movie.insert()

        res = self.client().patch('/movies/15', headers={
            'Authorization': bearer_tokens['casting_director']},
            json={'title': 'Update Movie'}
        )
        data = res.get_json()
        movie = Movie.query.filter(Movie.id == 15).one_or_none()
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.title, 'Update Movie')

        actor.delete()
        movie.delete()

    def test_delete_actor(self):
        actor = Actor(
            name='Delete Actor',
            gender='Male',
            age=25,
        )
        actor.id = 20
        actor.insert()

        res = self.client().delete('/actors/20', headers={
            'Authorization': bearer_tokens['casting_director']},
        )

        data = res.get_json()
        actor = Actor.query.filter(Actor.id == 20).one_or_none()
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_delete_movie(self):
        # Create movie to delete
        movie = Movie(
            release_date=date.today(),
            title='Test Movie'
        )
        movie.id = 20
        movie.insert()

        # Test movie delete
        res = self.client().delete('/movies/20', headers={
            'Authorization': bearer_tokens['executive_producer']},
        )
        data = res.get_json()
        movie = Movie.query.filter(Movie.id == 20).one_or_none()
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_post_movie(self):
        # Add actor to link to movie
        actor = Actor(
            name='Delete Actor',
            gender='Male',
            age=25,
        )
        actor.id = 20
        actor.insert()

        # New movie data
        new_movie = {
            'title': 'Test Movie Create',
            'release_date': '2020-01-01',
            'actor_id': '20'
        }

        # Test new movie created
        resp = self.client().post('/movies', headers={
            'Authorization': bearer_tokens['executive_producer']},
            json=new_movie
        )
        movie = Movie.query.filter(Movie.title == 'Test Movie Create').one_or_none()
        data = resp.get_json()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], movie.title)

        # Delete created movie and actor
        actor.delete()
        movie.delete()


if __name__ == "__main__":
    unittest.main()