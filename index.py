from flask import render_template, flash, request, redirect, url_for
from my_forms import Words_Form, Log_inForm, User_Form
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user, login_required, logout_user
from game import *
from models import *

#### Game ####


@app.route('/')
def index():
    global hits
    global lives
    global points
    hits = 0
    lives = 0
    points = 0
    our_users = Users.query.order_by(desc(Users.record)).limit(10).all()
    return render_template('index.html', users=our_users)

@app.route("/categories/")
def categories():
    categories =  Words.query.order_by(Words.id)
    return render_template('categories.html',
                categories=categories)

@app.route("/game/<string:category>")
def game(category):
    global word
    global category1
    global lines
    global hits
    parameters = Hangman.parameters(category)
    word = parameters['word_to_guess']
    category1 = parameters['category']
    lines = parameters['lines']
    to_hits = parameters['to_hits']
    hits = to_hits
    return render_template("playing.html",
                    category = category,
                    word_to_guess = parameters['word_to_guess'],
                    letters = parameters['letters'],
                    lines = parameters['lines'],                   
                    image = 'lives0')

@app.route("/playing/<string:id>", methods=['GET','POST'])
def playing(id):
    global lines
    global lives
    global hits
    global message
    global points
    game_stars = Hangman(word, lives, lines, hits, message, points) 
    playing_game = game_stars.progress(id)
    lines = playing_game['lines']
    lives = playing_game['lives']
    hits = playing_game['hits']
    message = playing_game['message']
    points = playing_game['points']
    image = Hangman.images(lives)
    if hits == len(word):
        message = 'Congratulations!!!... You WINN!!!'
        lives = 0
        lines = ''
        hits = 0
        return render_template('result.html', message = message, points = points)
    elif lives >= 5:
        message = 'Sorry... You Lost!'
        lives = 0
        lines = ''
        hits = 0
        return render_template('result.html', message = message, points = points)

    else:
        
        if message == None:
            return render_template('playing.html',
                            category = category1,
                            letters = letters,
                            lines = lines,                   
                            image = image,
                            message = message,
                            points = points)
        elif message == 'Letter alredy used...':
            return render_template('playing.html',
                            category = category1,
                            letters = letters,
                            lines = lines,                   
                            image = image,
                            message = message,
                            points = points)
        else:
            return render_template('result.html', message = message, points = points)
   
@app.route('/admin', methods=['GET','POST'])
def admin():
    form = Words_Form()
    if form.validate_on_submit():
        category = Words(category=form.category.data, words=form.words.data)
        form.category.data = ''
        form.words.data = ''
        db.session.add(category)
        db.session.commit()
        flash('Category Submitted Successfully')
    categories = Words.query.order_by(Words.id)
    our_users = Users.query.order_by(Users.date_created)
    return render_template ('admin.html',
                    form=form,
                    categories=categories,
                    our_users=our_users)

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
                return redirect(url_for('player_profile'))
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
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    form = Words_Form()
    categories = Words.query.order_by(Words.id)
    our_users = Users.query.order_by(Users.date_created)

    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'User {user_to_delete.username} deleted successfully...')
    our_users = Users.query.order_by(Users.date_created)
    return render_template('admin.html',
                        form=form,
                        our_users = our_users,
                        categories=categories)

@app.route('/delete_caetgory/<int:id>')
def delete_category(id):
    name=None
    category_to_delete = Words.query.get_or_404(id)
    form = Words_Form()
    categories =  Words.query.order_by(Words.category)
    our_users = Users.query.order_by(Users.date_created)
    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        flash('Category deleted successfully...')

        return render_template('admin.html')
    except:
        flash('Could not delete anthing...')
        return render_template('admin.html',
                            form=form,
                            name=name,
                            categories=categories,
                            our_users = our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):  
    form = User_Form()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.record = request.form['record']
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
                            
@app.route('/player_profile')
@login_required
def player_profile():
    return render_template('player_profile.html', points=points)

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = User_Form()
    user = Users.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():                     
        if username_exists(form.username.data):
            flash(f'username "{form.username.data}" alredy exists...')
            return render_template('add_user.html',
                        form=form,
                        name=name)  
        elif email_exists(form.email.data):
            flash(f'email "{form.email.data}" alredy exists...')
            return render_template('add_user.html',
                        form=form,
                        name=name)       
        elif user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(username=form.username.data, email=form.email.data, password_hash=hashed_pw, record=0)
            db.session.add(user)
            db.session.commit()
            flash('User Added Successfully')        
        else:
            flash(f'Oops... seems something went wrong... Try again...')
            return render_template('add_user.html',
                        form=form,
                        name=name)       
        name = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''   
    return render_template('add_user.html',
                        form=form,
                        name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/save_points/<int:id>', methods=['GET', 'POST'])
@login_required
def save_points(id):
    global points
    user_update =  Users.query.get_or_404(id)
    if user_update:
        user_update.record += points
        db.session.commit()
        points = 0
        flash('Submitted Successfully!')
    else:
        flash('error!')
    return render_template('player_profile.html')