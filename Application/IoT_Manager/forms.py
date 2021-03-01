from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from IoT_Manager.sql_models import User, Trigger_Types
from IoT_Manager import app, db_session


class SignUpForm(FlaskForm):
    """Form for creating a new user"""

    email = StringField(
        "Email", validators=[DataRequired(),
                             Length(min=3, max=80),
                             Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = db_session.query(User).filter_by(email=self.email.data).first()
        if user:
            raise ValidationError(
                'That email is already in use by a different account.')


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    email = StringField(
        "Email", validators=[DataRequired(),
                             Length(min=3, max=80),
                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class CreateDeviceForm(FlaskForm):
    """Form for creating new device"""
    device_code = StringField('Device Code')
    name = StringField('Name')
    desc = TextAreaField('Description')
    create = SubmitField('Create')

class CreateTriggerForm(FlaskForm):
    """Form for creating new trigger"""
    trigger_type = SelectField('Tigger Type', choices=[(member.value, name.capitalize()) for name, member in Trigger_Types.__members__.items()])
    name = StringField('Name')
    desc = TextAreaField('Description')
    create = SubmitField('Create')
