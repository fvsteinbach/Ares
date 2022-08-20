from flask import Flask, request, render_template, redirect
from cs50 import SQL
from datetime import date

app = Flask(__name__)

db = SQL("sqlite:///students.db")

STUDENTS = {}

BELTS = ["No belt", "White", "Blue", "Purple", "Brown", "Black"]
DEGREES = ["No degree","I", "II", "III", "IV"]

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html", belts=BELTS, degrees=DEGREES)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/registrants", methods=["POST"])
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

    #Confirm registration
    return redirect ("/students")

@app.route("/students")
def students():
    students = db.execute("SELECT * FROM students")
    return render_template("students.html", students=students)

@app.route("/deregister", methods=["POST"])
def deregister():
    
    #Delete student
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM students WHERE id = ?", id)
    return redirect("/students")

if __name__==("__main__"):
    app.run()