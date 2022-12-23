from flask import Flask, render_template, flash, request, redirect, url_for
from my_forms import Words_Form, Log_inForm, User_Form, Name
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from dataclasses import dataclass
from random import choice


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/hangman_users'
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#print('hello', db.Model)
#Model
log_in_manager = LoginManager()
log_in_manager.init_app(app)
log_in_manager.login_view = 'log_in'
letters = [chr(i) for i in range(65,91)]

@log_in_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Models

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(200))

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

class Words(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(56), nullable=False, unique=True)
    words = db.Column(db.Text)


def email_exists(email):
    return Users.query.filter_by(email=email).first() is not None
def username_exists(username):
    return Users.query.filter_by(username=username).first() is not None

# Game
hits = []
letters = [chr(i) for i in range(65,91)]
lives = 0


@dataclass
class Game:
    letter: str 
    word: str
    lines: str
    lives: int
    hits: list

    def word_to_guess(words):
        words_list = words.split()
        word = choice(words_list)
        #word = words_list[1]
        cleaned_word = {
            ord(","):None,
            ord("'"):None,
            ord("["):None,
            ord("]"):None}
        word = word.translate(cleaned_word)
        return word

    def playing(self):       
        uploaded_lines = self.lines              
        if self.letter in self.word:                  
            for i in range(len(self.word)):  
                if self.letter == self.word[i]:                                       
                    uploaded_lines[i] = self.letter
                    self.hits.append(self.letter)
                else:
                    continue
            return {'lines': uploaded_lines,
                    'lives': self.lives,
                    'hits': self.hits }
        else:          
            return {'lines': uploaded_lines,
                    'lives': self.lives+1,
                    'hits': self.hits }
    
    def images(index):
        images_urls = f'lives{index}'
        return images_urls

@app.route("/categories/")
def categories():
    categories =  Words.query.order_by(Words.id)
    return render_template('categories.html',
                categories=categories)

@app.route("/game/<string:category>")
def game(category):
    global selected_category
    global word_to_guess
    global lines  
    selected_category=category   
    words_list =  Words.query.filter_by(category=selected_category).first()
    word_to_guess = Game.word_to_guess(words_list.words)
    lines = ["_" for i in range(len(word_to_guess))]
    return render_template("playing.html",
                    category=selected_category,
                    word_to_guess=word_to_guess,
                    letters = letters,
                    lines=lines,                   
                    image = 'lives0')
  
@app.route("/playing/<string:id>", methods=['GET','POST'])
def playing(id):
    letter = id 
    global lines
    global image
    global lives
    global hits
    if len(hits) < len(word_to_guess)-1:
        if lives < 4:
            data = Game(letter, word_to_guess, lines, lives, hits)
            progress = data.playing()   
            lines = progress['lines']
            lives = progress['lives']
            hits = progress['hits']
            image = Game.images(lives)
            return render_template("playing.html",
                        letters=letters,
                        category=selected_category,                                           
                        lines=lines,
                        lives=lives,                       
                        image=image,
                        progress = hits,
                        word_to_guess=word_to_guess)
        else:
            hits = [] 
            lives = 0
            message = 'Sorry... You lost!'
            return render_template("result.html", message= message)
       
    else:
        hits = [] 
        lives = 0
        message = 'Congratulations!!!... You WINN!!!'
        return render_template("result.html", message= message)  
    
@app.route('/add_words', methods=['GET','POST'])
def add_words():
    form = Words_Form()
    if form.validate_on_submit():
        category = Words(category=form.category.data, words=form.words.data)
        form.category.data = ''
        form.words.data = ''
        db.session.add(category)
        db.session.commit()
        flash('Category Submitted Successfully')
    categories = Words.query.order_by(Words.id)
    return render_template ('add_words.html',
                    form=form,
                    categories=categories)

@app.route('/result')

def result():
    global hits
    global lives
    hits = []
    lives = 0
    categories =  Words.query.order_by(Words.id)
    return render_template ('categories.html',
                categories=categories)
                 
@app.route('/log_in', methods=['GET','POST'])
def log_in():
    form = Log_inForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f'Hello {user.username}!')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect Password... Try Again!')
        else:
            flash('User does not exist...')
    return render_template('log_in.html',form=form)

@app.route('/log_out', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    flash('Yoy have loged out, come back soon!')
    return redirect(url_for('log_in'))

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

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
@login_required
def update(id):  
    form = User_Form()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.username = request.form['username']
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
    global hits
    global lives
    hits = []
    lives = 0
    return render_template('index.html')
                            
@app.route('/user/<name>')
def user(name):
    return render_template('player_profile.html', name=name)

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = User_Form()
    user = Users.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():            
         
        if username_exists(form.username.data):
            flash(f'username "{form.username.data}" alredy exists...')
            our_users = Users.query.order_by(Users.date_created)
            return render_template('add_user.html',
                        form=form,
                        name=name,
                        our_users = our_users)  
        elif email_exists(form.email.data):
            flash(f'email "{form.email.data}" alredy exists...')
            our_users = Users.query.order_by(Users.date_created)
            return render_template('add_user.html',
                        form=form,
                        name=name,
                        our_users = our_users)
        
        elif user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('User Added Successfully')
        
        else:
            flash(f'Oops... seems something went wrong... Try again...')
            our_users = Users.query.order_by(Users.date_created)
            return render_template('add_user.html',
                        form=form,
                        name=name,
                        our_users = our_users)
        
        name = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
    
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
