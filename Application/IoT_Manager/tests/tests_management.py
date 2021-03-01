import os
import unittest
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



class MainTests(unittest.TestCase):
 

    user_email = 'test2@test.org'
    user_password = 'password'

    device_name = 'device_name_test'
    trigger_name = 'trigger_name_test'

    def create_user(self):
        user = User(email=self.user_email, password=self.user_password)
        db_session.add(user)
        db_session.commit()
        return user

    def create_device(self, user):
        device = Device(
            user=user,
            device_code="device_code_test",
            name=self.device_name,
            desc="desc_test"
        )
        db_session.add(device)
        db_session.commit()
        return device


    def create_trigger(self, device):
        trigger = Trigger(
            device=device,
            trigger_type='MAGNETOMETER',
            name=self.trigger_name,
            desc="desc_test"
        )
        db_session.add(device)
        db_session.commit()
        return device

    def login(self):
        return self.app.post('/login', data=dict(
            email=self.user_email,
            password=self.user_password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

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

    def test_create_device(self):
        self.create_user()
        self.login()
        data = {
            'device_code':'sadfkasdkjasldfjla',
            'name':self.device_name,
            'desc':'fsadfsa dfs alkdjfsajdfkjaslkdfjlasdj kfaj kasdjfk'
        }
        resp = self.app.post('/management/panel',
            follow_redirects=True,
            data=data
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(db_session.query(Device).filter_by(name=self.device_name).first())

    def test_get_main_panel(self):
        user = self.create_user()
        self.login()
        self.create_device(user)
        response = self.app.get('/management/panel', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('Create Device', response_text)
        self.assertIn(self.device_name, response_text)

    def test_create_trigger(self):
        user = self.create_user()
        self.login()
        device = self.create_device(user)
        credentials = {
            'trigger_type':'0',
            'name':self.trigger_name,
            'desc':'fsadfsa dfs alkdjfsajdfkjaslkdfjlasdj kfaj kasdjfk'
        }
        resp = self.app.post('/management/panel/{0}'.format(device.id),
            follow_redirects=True,
            data=credentials
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(db_session.query(Trigger).filter_by(name=credentials['name']).first())


    def test_get_device_panel(self):
        user = self.create_user()
        self.login()
        device = self.create_device(user)
        self.create_trigger(device)
        response = self.app.get('/management/panel/{0}'.format(device.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('Create Trigger', response_text)
        self.assertIn(self.trigger_name, response_text)