from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from calendarapp.models import User, Event


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That user is taken. Please chose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please chose a diffrent one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class EventForm(FlaskForm):
    description = StringField("Name", validators=[DataRequired(), Length(min=1, max=100)])
    start_time = StringField("Start Time (hh:mm)", validators=[DataRequired()])
    duration = DecimalField("Duration (min)", validators=[DataRequired(), NumberRange(min=0.0001, max=1440)])
    submit = SubmitField("Add event")

    def validate_start_time(self, start_time):
        valid = False
        st = start_time.data
        if len(st) == 5:
            try:
                if 0 <= int(st[:2]) < 24 and 0 <= int(st[3:]) < 60 and st[2] == ":":
                    valid = True
            
            except:
                pass

        if not valid:
            raise ValidationError("Please enter the date in the correct format")


    def validate_description(self, description):
        event = Event.query.filter_by(description=description.data).first()
        if event:
            raise ValidationError("Please chose a unique name")
