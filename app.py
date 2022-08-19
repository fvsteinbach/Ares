from flask import Flask, request, render_template, redirect

app = Flask(__name__)

fighters = {}

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
    #Validate name
    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing name")
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

    fighters[name] = belt

    return render_template("registrants.html", name=name)

if __name__==("__main__"):
    app.run()