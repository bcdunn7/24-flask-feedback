from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    username = db.Column(db.Text,
                    primary_key=True)

    password = db.Column(db.Text,
                    nullable=False)

    email = db.Column(db.String(50), 
                    unique=True,
                    nullable=False)

    first_name = db.Column(db.String(30),
                    nullable=False)

    last_name = db.Column(db.String(30),
                    nullable=False)


    @classmethod
    def register(cls, username, pswd, email, first, last):
        """Register user."""

        hashed_pswd = bcrypt.generate_password_hash(pswd).decode('utf-8')

        return cls(username=username, password=hashed_pswd, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pswd):
        """Authenticate user."""

        usr = User.query.filter_by(username=username).first()
        
        if usr and bcrypt.check_password_hash(usr.password, pswd): 
            return usr
        else:
            return False
            


class Feedback(db.Model):
    """Feedback model."""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, 
                primary_key=True, 
                autoincrement=True)

    title = db.Column(db.String(50),
                nullable=False)

    content = db.Column(db.Text,
                nullable=False)

    username = db.Column(db.Text, 
                db.ForeignKey('users.username'))

    user = db.relationship('User', backref=db.backref('feedback', cascade='all, delete-orphan'))