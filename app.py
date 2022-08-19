from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

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
    return render_template("registrants.html", name=name)

if __name__==("__main__"):
    app.run()