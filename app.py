from flask import Flask, request, render_template, redirect, session, flash
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, DateField, SelectField
from wtforms.validators import data_required,input_required
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from cs50 import SQL

BELTS = ["No belt", "White", "Blue", "Purple", "Brown", "Black"]
DEGREES = ["No degree","I", "II", "III", "IV"]

#Configure app
app = Flask(__name__)
#Configure database
db = SQL('sqlite:///database.db')
#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Secret key
app.config["SECRET_KEY"] = "fuckthissecretkey"
Session(app)

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
    username_validation = db.execute("SELECT * FROM Users WHERE username == ?", username)
    if username_validation == []:
        email_validation = db.execute("SELECT * FROM Users WHERE email = ?", email)
        if email_validation == []:
            db.execute("INSERT INTO Users (first_name, last_name, birthdate, belt, degree, email, phone, username, date_added) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", first_name, last_name, birthdate, belt, degree, email, phone, username, date_added)
            flash("User added successfully")
            return redirect("/profile")
        return render_template("error.html", message="Email already been used")
    return render_template("error.html", message='Username already been used')

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
    users = db.execute("SELECT * FROM Users")
    return render_template("dashboard.html", users=users)

@app.route("/deregister", methods=["POST"])
def deregister():
    
    #Delete student
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM users WHERE id = ?", id)
    return redirect("/dashboard")

if __name__==("__main__"):
    app.run()