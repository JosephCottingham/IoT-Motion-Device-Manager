import os
from unittest import TestCase
import requests
from sqlalchemy import create_engine

from datetime import date
 
from IoT_Manager import app, db_session
from IoT_Manager.sql_models import (
    User,
    Device,
    Trigger,
    Event,
    Base
)


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
    user_email = 'test2@test.org'
    user_password = 'password'
    

    def create_user(self):
        user = User(email=self.user_email, password=self.user_password)
        db_session.add(user)
        db_session.commit()
        return user

    def login_user(self):
        credentials = {
            'email':self.user_email,
            'password':self.user_password
        }
        resp = self.app.post('/login',
            follow_redirects=True,
            data=credentials
        )
        return user

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
        Base.metadata.drop_all(db_engine)
        Base.metadata.create_all(db_engine)

    def tearDown(self):
        db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
        Base.metadata.drop_all(db_engine)

    def test_signup(self):
        credentials = {
            'email':self.user_email,
            'password':self.user_password
        }
        resp = self.app.post('/signup',
            follow_redirects=True,
            data=credentials
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(db_session.query(User).filter_by(email=credentials['email']).first())

    def test_login(self):
        user = self.create_user()
        credentials = {
            'email':self.user_email,
            'password':self.user_password
        }
        resp = self.app.post('/login',
            follow_redirects=True,
            data=credentials
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('/login' in str(resp.data))

    def test_logout(self):
        user = self.create_user()
        credentials = {
            'email':self.user_email,
            'password':self.user_password
        }
        resp = self.app.post('/login',
            follow_redirects=True,
            data=credentials
        )
        resp = self.app.get('/logout',
            follow_redirects=True
        )
        self.assertEqual(resp.status_code, 200)
