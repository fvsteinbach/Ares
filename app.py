from flask import Flask, request, render_template, redirect, session, flash
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, DateField, SelectField
from wtforms.validators import data_required,input_required
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

#Configure app
app = Flask(__name__)
#Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Secret key
app.config["SECRET_KEY"] = "fuckthissecretkey"
Session(app)

#Initiate database
db = SQLAlchemy(app)

#Create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    belt = db.Column(db.String, nullable=False)
    degree = db.Column()
    email = db.Column()
    phone = db.Column()
    username = db.Column()
    submit = db.Column()
    date_added = db.Column()


BELTS = ["No belt", "White", "Blue", "Purple", "Brown", "Black"]
DEGREES = ["No degree","I", "II", "III", "IV"]


#Create a Form class
class register_form(FlaskForm):
    first_name = StringField("What is your first name?", validators=[data_required()])
    last_name = StringField("What is your last name?", validators=[data_required()])
    birthdate = DateField("What is your birthdate?", validators=[data_required()])
    belt = SelectField("What is your current belt?", choices=["No belt", "White", "Blue", "Purple", "Brown", "Black"], validators=[data_required()])
    degree = SelectField("What is your current belt?", choices=["No degree","I", "II", "III", "IV"], validators=[data_required()])
    email = EmailField("What is your email?", validators=[data_required()])
    phone = TelField("What is your phone number?", validators=[data_required()])
    username = StringField("Create an Username?", validators=[data_required()])
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
    first_name = None
    last_name = None
    birthdate = None
    belt = None
    degree = None
    email = None
    phone = None
    username = None
    form = register_form()
        
    return render_template("signup.html",first_name=first_name, form=form, belt=belt, last_name=last_name, birthdate=birthdate, degree=degree, email=email, phone=phone, username=username)

@app.route("/profile", methods=["POST", "GET"])
def profile():
    flash("Form submited successfully!")
    return render_template("profile.html")

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