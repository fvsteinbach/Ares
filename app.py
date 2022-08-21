from sqlite3 import Date
from unicodedata import name
from flask import Flask, request, render_template, redirect, session, flash
from cs50 import SQL
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, DateField, SelectField
from wtforms.validators import data_required,input_required
from flask_session import Session

#Configure app
app = Flask(__name__)

#Configure database
db = SQL("sqlite:///students.db")

#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "fuckthissecretkey"
Session(app)

BELTS = ["No belt", "White", "Blue", "Purple", "Brown", "Black"]
DEGREES = ["No degree","I", "II", "III", "IV"]


#Create a Form class
class register_form(FlaskForm):
    name = StringField("What is your name?", validators=[data_required()])
    submit = SubmitField("Register")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html", belts=BELTS, degrees=DEGREES)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    name = None
    form = register_form()
    #Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''


    return render_template("signup.html",name = name, form = form)

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html", name=name)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    return render_template("/user.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("fname"):   
        return redirect("/register")
    students = db.execute("SELECT * FROM students")
    return render_template("dashboard.html", students=students)

@app.route("/deregister", methods=["POST"])
def deregister():
    
    #Delete student
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM students WHERE id = ?", id)
    return redirect("/dashboard")

if __name__==("__main__"):
    app.run()