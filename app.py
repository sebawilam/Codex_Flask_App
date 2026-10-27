from flask import Flask, render_template

app = Flask(__name__, static_folder=None)

LINKS = [
    ("Python", "https://www.python.org/"),
    ("Flask", "https://flask.palletsprojects.com/"),
    ("GitHub", "https://github.com/"),
]


@app.get("/")
def index():
    return render_template("index.html", links=LINKS)


@app.get("/about")
def about():
    return render_template("about.html")
