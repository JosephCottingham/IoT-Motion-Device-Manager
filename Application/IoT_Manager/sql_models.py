import uuid
import enum
from datetime import datetime, timedelta
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    BigInteger,
    Text,
    Enum
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash, gen_salt

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Trigger_Types(enum.Enum):
    """
    The diffrent trigger types (currently setup for connecting to general IMU device)
    """
    ACCELEROMETER=0
    MAGNETOMETER=1
    GYROSCOPE=2

class User(Base, UserMixin):
    """
    Model for users
    """

    __tablename__ = 'users'

    # Object referencing
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Modifcation/Creation tracking
    created_datetime = Column(DateTime(timezone=True), default=datetime.utcnow())
    modified_datetime = Column(DateTime(timezone=True), onupdate=datetime.utcnow())

    email = Column(String(64), index=True, unique=True)
    password_hash = Column(String(128), index=False)

    first_name = Column(String(32), index=False)
    last_name = Column(String(32), index=False)

    phone_num = Column(String(10), index=False)
    phone_country = Column(String(3), index=False)

    devices = relationship('Device', back_populates='user')

    def __init__(self, email, password, first_name=None, last_name=None, phone_num=None, phone_country=None):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone_num = phone_num
        self.phone_country = phone_country

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

class Device(Base):
    """
    Model IoT device
    """

    __tablename__ = 'devices'

    # Object referencing
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Code of IoT device to connect this DB device with real world IoT device
    device_code = Column(String(16), unique=True, nullable=False)
    
    # Modifcation/Creation tracking
    created_datetime = Column(DateTime(timezone=True), default=datetime.utcnow())
    modified_datetime = Column(DateTime(timezone=True), onupdate=datetime.utcnow())

    name = Column(String(32), index=False)
    desc = Column(String(32), index=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='devices')

    triggers = relationship('Trigger', back_populates='device')


    def __init__(self, user, device_code, name, desc):
        self.user = user
        self.device_code = device_code
        self.name = name
        self.desc = desc


class Trigger(Base):
    """
    Model IoT trigger
    """
    __tablename__ = 'triggers'

    # Object referencing
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Modifcation/Creation tracking
    created_datetime = Column(DateTime(timezone=True), default=datetime.utcnow())
    modified_datetime = Column(DateTime(timezone=True), onupdate=datetime.utcnow())

    name = Column(String(32), index=False)
    desc = Column(String(32), index=False)
 
    device_id = Column(Integer, ForeignKey('devices.id'))
    device = relationship('Device', back_populates='triggers')

    trigger_type = Column(Enum(Trigger_Types))

    events = relationship('Event', back_populates='trigger')


    def __init__(self, name, desc, device, trigger_type):
        self.name = name
        self.desc = desc
        self.device = device
        self.trigger_type = trigger_type

class Event(Base):
    """
    Model event which are generated when a IoT device reports back an action that alines with a trigger
    """

    __tablename__ = 'events'

    # Object referencing
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Modifcation/Creation tracking
    created_datetime = Column(DateTime(timezone=True), default=datetime.utcnow())
    modified_datetime = Column(DateTime(timezone=True), onupdate=datetime.utcnow())

    name = Column(String(32), index=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow())
 
    trigger_id = Column(Integer, ForeignKey('triggers.id'))
    trigger = relationship('Trigger', back_populates='events')


    def __init__(self, name, trigger, device, tigger_type, timestamp=None):
        self.name = name
        self.trigger = trigger
        if timestamp != None:
            self.timestamp = timestamp
