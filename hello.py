from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create a Flask instance
app = Flask(__name__)
#  add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# secret key
app.config['SECRET_KEY'] = 'my secret key nobody needs to know'
# initialize the db
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name

# Create form class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit =  SubmitField('Submit')

# Create form class
class NamerForm(FlaskForm):
    name = StringField('Whats your name', validators=[DataRequired()])
    submit =  SubmitField('Submit')

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',form=form,name=name,our_users=our_users)

@app.route('/')
def index():
    first_name= 'Chunks'
    # stuff = 'This is <strong>Bold</strong> Text' ** wotks with safe and striptag
    stuff = 'This is Bold Text'
   
    
    return render_template('index.html', 
   
    )

@app.route('/user/<name>')

def user(name):
    return render_template('user.html',user_name=name)


# Create Name page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully')
    return render_template('name.html',
    name = name,
    form = form
    )
