import os, json
from flask import Flask, render_template
from sqlalchemy import create_engine
from IoT_Manager.config import Config
import datetime
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, current_user

config = Config.get_instance()

##################
### APP CONFIG ###
##################

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = config.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
#### DATABASE ####
##################

from .sql_models import (
    User,
    Device,
    Trigger,
    Event,
    Base
)

# SQLALCHEMY Setup
db_engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

# create metadata
Base.metadata.create_all(db_engine)

# create session
Session = sessionmaker(bind=db_engine)
db_session = Session()
db_session.commit()

app.config['SQLALCHEMY_SESSION'] = db_session

##################
###### AUTH ######
##################
login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "user.login"

@login_manager.user_loader
def load_user(id):
    return db_session.query(User).get(id)


##################
##### ROUTES #####
##################

from .views.user import User_Blueprint
from .views.management import Management_Blueprint

app.register_blueprint(User_Blueprint, url_prefix='')
app.register_blueprint(Management_Blueprint, url_prefix='/management')

@app.route("/")
def home():
    return render_template('home.html')

@app.after_request
def after_request(response):    
    return response
