from flask import Flask, request, render_template, redirect, session
from cs50 import SQL
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField
from wtforms.validators import data_required,input_required
from flask_session import Session

#Configure app
app = Flask(__name__)

#Configure database
db = SQL("sqlite:///students.db")

#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BELTS = ["No belt", "White", "Blue", "Purple", "Brown", "Black"]
DEGREES = ["No degree","I", "II", "III", "IV"]

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html", belts=BELTS, degrees=DEGREES)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/registrants", methods=["POST","GET"])
def registrants():
    #Validate first name
    fname = request.form.get("fname")
    if not fname:
        return render_template("error.html", message="Missing first name")
    
    #Validate last name
    lname = request.form.get("lname")
    if not lname:
        return render_template("error.html", message="Missing last name")
        
    #Validate birthdate
    birthdate = request.form.get("birthdate")
    if not birthdate:
        return render_template("error.html", message="Missing birthdate")
    
    #Validate fighter belt
    belt = request.form.get("belt")
    if belt not in BELTS:
        return render_template("error.html", message="Missing belt")
    
    #Validate fighter belt degree
    degree = request.form.get("degree")
    if degree not in DEGREES:
        return render_template("error.html", message="Missing belt degree")

    #Validate email
    email = request.form.get("email")
    if not email:
        return render_template("error.html", message="Missing email")

    #Validate phone
    phone = request.form.get("phone")
    if not phone:
        return render_template("error.html", message="Missing phone")


    #Get student age
    birthyear = int(birthdate[:4])
    thisyear = date.today().year
    age = thisyear - birthyear

    #Remember student
    db.execute("INSERT INTO students (fname, lname, belt, degree, age, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)", fname, lname, belt, degree, age, phone, email)

    #Saves the data on a session
    if request.method == "POST":
        session["fname"] = request.form.get("fname")
        return redirect("/dashboard")

    #Confirm registration
    return render_template("user.html", fname=fname)

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