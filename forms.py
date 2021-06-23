from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    """Form for registering new user."""

    username = StringField("Username",
                        validators=[InputRequired(message="Username can't be blank")])

    password = PasswordField("Password",
                        validators=[InputRequired(message="Password can't be blank")])

    email = StringField("Email",
                        validators=[InputRequired(message="Email can't be blank"), Email(message="Not valid email"), Length(max=50, message="Too many characters")])

    first_name = StringField("First Name",
                        validators=[InputRequired(message="First Name can't be blank"), Length(max=30, message="Too many characters")])

    last_name = StringField("Last Name",
                        validators=[InputRequired(message="Last Name can't be blank"), Length(max=30, message="Too many characters")])


class LoginUserForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Username",
                        validators=[InputRequired(message="Username can't be blank")])

    password = PasswordField("Password",
                        validators=[InputRequired(message="Password can't be blank")])


class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField("Title",
                        validators=[InputRequired(message="Title can't be blank"), Length(max=50, message="Max length: 50 character")])

    content = StringField("Content",
                        validators=[InputRequired(message="Content can't be blank")])