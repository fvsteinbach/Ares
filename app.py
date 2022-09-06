from flask import Flask, request, render_template, redirect, session, flash
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, DateField, SelectField, BooleanField, ValidationError
from wtforms.validators import data_required,input_required, equal_to, length, email_validator
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

#Flask_login   
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))



#Create a model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    belt = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)
    username =  db.Column(db.String(25), nullable=False, unique=True)
    #Hashing password
    password_hash = db.Column(db.String(), nullable=False)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



    date_added = db.Column(db.Date, default=datetime.utcnow)
    
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
    password_hash = PasswordField("Create a password", validators=[data_required(), equal_to('password_hash_val', message='Passwords must match!')])
    password_hash_val = PasswordField("Confirm your password", validators=[data_required(), equal_to('password_hash', message='Passwords must match!')])
    submit = SubmitField("Register")


#Create a login Form
class login_form(FlaskForm):
    username = StringField("What is your username?", validators=[data_required()])
    password = PasswordField("What is your password?", validators=[data_required()])
    submit = SubmitField("Login")

#Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

#Login page
@app.route("/login", methods=['POST', 'GET'])
def login():
    form = login_form()
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        #Checks if theres an user with the username inputed
        if user:
            password_check = form.password.data
            #Clear the form
            form.username.data = ''
            form.password.data = ''
            #Check hashed password
            if check_password_hash(user.password_hash, password_check):
                login_user(user)
                flash("Login successfully!")
                return redirect("/profile", form=form, user=user)
            else:
                flash("Wrong password")
        else:
            flash("That username does not exist, try again")
    return render_template("login.html", form=form)

#Create logout page
@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect("/login")

#Signup route
@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = register_form()
    return render_template("signup.html", first_name=form.first_name.data, form=form, belt=form.belt.data, last_name=form.last_name.data, birthdate=form.birthdate.data, degree=form.degree.data, email=form.email.data, phone=form.phone.data, username=form.username.data, password_hash=form.password_hash.data)

#Register route
@app.route("/register", methods=["POST", "GET"])
def register():
    first_name = None
    form = register_form()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data, username=form.username.data, phone=form.phone.data).first()
        if user is None:
            #Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = users(first_name=form.first_name.data, last_name=form.last_name.data, birthdate=form.birthdate.data, belt=form.belt.data,
            degree=form.degree.data, email=form.email.data, phone=form.phone.data, username=form.username.data, password_hash=hashed_pw, date_added=date.today())
            db.session.add(user)
            db.session.commit()
            print(hashed_pw)
        first_name = form.first_name.data
        form.first_name.data = ''
        form.last_name.data  = ''
        form.birthdate.data = ''
        form.belt.data = ''
        form.degree.data = ''
        form.email.data = ''
        form.phone.data = ''
        form.username.data = ''
        form.password_hash.data = ''
        form.password_hash_val.data = ''
        flash("User created successfully")
        return render_template("profile.html", form=form, user=user, first_name=first_name)
    our_users = users.query.order_by(users.date_added)   
    return redirect("/dashboard", our_users)

#Route to the profile page
@app.route("/profile", methods=["POST", "GET"])
def profile():
    form = login_form()
    user = users.query.filter_by(username = form.username.data)
    return render_template("profile.html", form=form, user=user)

#Route to update an existing user
@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    form = register_form()
    name_update = users.query.get_or_404(id)
    if request.method == 'POST':
        name_update.first_name = request.form['first_name']
        name_update.last_name = request.form['last_name']
        date_birthdate = request.form['birthdate']
        #Makes converts the old date back to string (when imported from the database it becomes a strin so it needs to be converted)
        name_update.birthdate = datetime.strptime(f'{date_birthdate}', '%Y-%m-%d').date()
        name_update.belt = request.form['belt']
        name_update.degree = request.form['degree']
        name_update.email = request.form['email']
        name_update.phone = request.form['phone']
        name_update.username = request.form['username']
        hashed_pw = generate_password_hash(request.form['password_hash'], 'sha256')
        name_update.password_hash = hashed_pw
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("update.html", form=form, name_update=name_update)
        except:
            flash("Error! Looks like there was a problem")
            return render_template("update.html", form=form, name_update=name_update)
    return render_template("update.html", form=form, name_update=name_update)

@app.route("/error")
def error():
    return render_template("error.html")

#DASHBOARD ROUTE
@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    our_users = users.query.order_by(users.date_added)
    return render_template("dashboard.html", our_users=our_users)

@app.route("/deregister/<int:id>", methods=["POST"])
def deregister(id):
    user_delete = users.query.get_or_404(id)
    
    try:
       db.session.delete(user_delete)
       db.session.commit()
       return redirect("/dashboard")
    except:
        return redirect("/dashboard")


if __name__==("__main__"):
    app.run()