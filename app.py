from crypt import methods
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

if __name__==("__main__"):
    app.run(debug=True)