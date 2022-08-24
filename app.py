from flask import Flask, request, render_template, redirect, session, flash, url_for
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
    username =  db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    belt = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.Date, default=datetime.utcnow)

    #Create a string
    def __repr__(self):
        return '<Name %r>' %self.first_name


#Create a Form class
class register_form(FlaskForm):
    first_name = StringField("What is your first name?", validators=[data_required()])
    last_name = StringField("What is your last name?", validators=[data_required()])
    username = StringField("Create an Username", validators=[data_required()])
    belt = SelectField("What is your current belt?", choices=["No belt", "White", "Blue", "Purple", "Brown", "Black"], validators=[data_required()])
    degree = SelectField("What is your current belt?", choices=["No degree","I", "II", "III", "IV"], validators=[data_required()])
    email = EmailField("What is your email?", validators=[data_required()])
    phone = TelField("What is your phone number?", validators=[data_required()])
    birthdate = DateField("What is your birthdate?", validators=[data_required()])
    password = PasswordField("Enter your password", validators=[data_required()])
    submit = SubmitField("Register")
    update = SubmitField("Update")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = register_form()
    return render_template("signup.html", form=form, first_name=form.first_name.data, last_name=form.last_name.data,
    birthdate=form.birthdate.data, belt=form.belt.data,  degree=form.degree.data, email=form.email.data,
    phone=form.phone.data, username=form.username.data)

@app.route("/register", methods=["POST"])
def register():
    form = register_form()
    if form.validate_on_submit():
        user = users(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, password=form.password.data, birthdate=form.birthdate.data, belt=form.belt.data, degree=form.degree.data, email=form.email.data, phone=form.phone.data, date_added=datetime.date().today())
        db.session.add(user)
        db.session.commit()
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
        users = users.query.order_by(users.date_added)   
    return redirect("/profile", users=users)

@app.route("/profile", methods=["POST", "GET"])
def profile():
    flash("Form submited successfully!")
    form = register_form()
    return render_template("profile.html", form=form)

#Update database
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    form = register_form()
    name_update = users.query.get_or_404(id)
    if request.method == "POST":
        name_update.first_name = request.form['first_name']
        name_update.last_name = request.form['last_name']
        name_update.email = request.form['email']
        name_update.phone = request.form['phone']
        name_update.username = request.form['username']
        name_update.birthdate = request.form['birthdate']
        name_update.belt = request.form['birthdate']
        name_update.degree = request.form['degree']
        try:
            db.session.commit()
            flash("User updated successfully")
            return redirect("/dashboard", form=form, name_update=name_update)
        except:
            flash("Error, looks like there was a problem...try again")
            return render_template("update.html", form=form, name_update=name_update)
    return render_template("update.html", form=form, name_update=name_update)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/dashboard")
def dashboard():
    our_users = users.query.order_by(users.date_added)
    return render_template("dashboard.html", our_users=our_users)

@app.route("/deregister", methods=["POST"])
def deregister():
    #Delete student
    if id:
        db.execute("DELETE FROM users WHERE id = ?", id)
    return redirect("/dashboard")

if __name__==("__main__"):
    app.run()

