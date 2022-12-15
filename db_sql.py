from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/hangman_users'
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#print('hello', db.Model)
#Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(120))

    @property
    def password(self):
        raise AttributeError('Password is unreadable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name
#Forms
class User_Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Name(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name=None
    form=User_Form()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully...')
        our_users = Users.query.order_by(Users.date_created)
        return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users = our_users)
    except:
        flash('Could not delete anthing...')
        return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users = our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = User_Form()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('User Updated Successfully')
            return render_template('update.html',
                        form=form,
                        name_to_update=name_to_update)
        except:
            db.session.commit()
            flash('Error! Looks like there was a problem... try again letter')
            return render_template('update.html',
                        form=form,
                        name_to_update=name_to_update)
    else:
        return render_template('update.html',
                        form=form,
                        name_to_update=name_to_update,
                        id=id)
@app.route('/')
def index():
    first_name = 'Mario'
    return render_template('index.html',
                            first_name=first_name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = User_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(name=form.name.data, email=form.email.data, pasword_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        password_hash = ''
        flash('User Added Successfully')
    our_users = Users.query.order_by(Users.date_created)
    return render_template('add_user.html',
                            form=form,
                            name=name,
                            our_users = our_users)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/user_name', methods=['GET', 'POST'])
def user_name():
    name = None
    form = Name()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Submitted Successfully!')

    return render_template('user_name.html',
                            name=name, 
                            form=form)

"""
if __name__=="__main__":
    app.run(debug=True)"""