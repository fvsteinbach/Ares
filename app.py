from email.policy import default
from enum import unique
from inspect import Attribute
from flask import Flask, request, render_template, redirect, session, flash
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, DateField, SelectField
from wtforms.validators import data_required,input_required
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

BELTS = ["No belt", "White", "Blue", "Purple", "Brown", "Black"]
DEGREES = ["No degree","I", "II", "III", "IV"]

#Configure app
app = Flask(__name__)
#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret key
app.config["SECRET_KEY"] = "fuckthissecretkey"
#Initialize the database
db = SQLAlchemy(app)

#Create a model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    belt = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False)
    username =  db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    #Create a string
    def __repr__(self) -> str:
        return super().__repr__()


#Create a Form class
class register_form(FlaskForm):
    first_name = StringField("What is your first name?", validators=[data_required()])
    last_name = StringField("What is your last name?", validators=[data_required()])
    birthdate = DateField("What is your birthdate?", validators=[data_required()])
    belt = SelectField("What is your current belt?", choices=["No belt", "White", "Blue", "Purple", "Brown", "Black"], validators=[data_required()])
    degree = SelectField("What is your current belt?", choices=["No degree","I", "II", "III", "IV"], validators=[data_required()])
    email = EmailField("What is your email?", validators=[data_required()])
    phone = TelField("What is your phone number?", validators=[data_required()])
    username = StringField("Create an Username", validators=[data_required()])
    password = PasswordField("Enter your password", validators=[data_required()])
    submit = SubmitField("Register")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = register_form()
    first_name=form.first_name.data
    last_name=form.last_name.data 
    birthdate=form.birthdate.data
    belt=form.belt.data
    degree=form.degree.data
    email=form.email.data
    phone=form.phone.data
    username=form.username.data
    password = form.password.data
    return render_template("signup.html", first_name=first_name, form=form, belt=belt, last_name=last_name, birthdate=birthdate, degree=degree, email=email, phone=phone, username=username)

@app.route("/register", methods=["POST", "GET"])
def register():
    form = register_form()
    first_name = None
    if form.validate_on_submit():
        first_name=form.first_name.data
        last_name=form.last_name.data 
        birthdate=form.birthdate.data
        belt=form.belt.data
        degree=form.degree.data
        email=form.email.data
        phone=form.phone.data
        username=form.username.data
        password = form.password.data
        date_added = datetime.today()
        user_email = users.query.filter_by(email=email)
        user_username = users.query.filter_by(username=username)
        user_password = users.query.filter_by(password=password)
        if user_email is None and user_username is None and user_password is None:
            user = users(first_name, last_name, birthdate, belt, degree, email, phone, username, password, date_added)
            db.session.add(user)
            db.commit()
        form.first_name.data = ''
        form.last_name.data  = ''
        form.birthdate.data = ''
        form.belt.data = ''
        form.degree.data = ''
        form.email.data = ''
        form.phone.data = ''
        form.username.data = ''
        form.password.data = ''
        flash("User created successfully")
    our_users = users.query.order_by(users.date_added)   
    return redirect("/profile")

@app.route("/profile", methods=["POST", "GET"])
def profile():
    flash("Form submited successfully!")
    form = register_form()
    return render_template("profile.html", form=form)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/dashboard")
def dashboard():
    our_users = users.query.order_by(users.date_added)
    print(our_users)
    return render_template("dashboard.html", our_users=our_users)

@app.route("/deregister", methods=["POST"])
def deregister():
    
    #Delete student
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM users WHERE id = ?", id)
    return redirect("/dashboard")

if __name__==("__main__"):
    app.run()