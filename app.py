from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

LINKS = [
    ("Python", "https://www.python.org/"),
    ("Flask", "https://flask.palletsprojects.com/"),
    ("GitHub", "https://github.com/"),
]


@app.get("/")
def index():
    return render_template("index.html", links=LINKS)


@app.post("/add")
def add_link():
    name = request.form["name"].strip()
    url = request.form["url"].strip()
    if not name or not url:
        abort(400)
    LINKS.append((name, url))
    return redirect(url_for("index"))


@app.get("/about")
def about():
    return render_template("about.html")
