from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea


class User_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    record = IntegerField('Record')
    submit = SubmitField('Submit')

class Password_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Log_inForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Words_Form(FlaskForm):
    category = StringField('Category', validators=[DataRequired()], render_kw={"placeholder": "Category name"})
    words = StringField('Words', validators=[DataRequired()], widget=TextArea(), render_kw={"placeholder": "Copy-paste or write a list of words in capital letters saparated by commas in the format '[WORD,SECOND_WORD,THIRD_WORD,PHRASE_WITH_SEVERAL_WORDS...etc]'. If it's a phrase, replace the space with an underscore."})
    submit = SubmitField('Submit')

class Leters_Form(FlaskForm):
    submit = SubmitField('Submit')
