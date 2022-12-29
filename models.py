from flask import Flask
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/hangman_users'
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

log_in_manager = LoginManager()
log_in_manager.init_app(app)
log_in_manager.login_view = 'log_in'


@log_in_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#### Models ####

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(200))
    record = db.Column(db.Integer, nullable=True, unique=False)

    @property
    def password(self):
        raise AttributeError('Password is unreadable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.username

class Words(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(56), nullable=False, unique=True)
    words = db.Column(db.Text)


def email_exists(email):
    return Users.query.filter_by(email=email).first() is not None
def username_exists(username):
    return Users.query.filter_by(username=username).first() is not None


