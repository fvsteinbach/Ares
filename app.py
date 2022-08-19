from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/registrants", methods=["GET", "POST"])
def registrants():
    name = request.args.get("name")
    return render_template("registrants.html", name=name)

if __name__==("__main__"):
    app.run()