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


@app.route("/edit/<int:link_index>", methods=["GET", "POST"])
def edit_link(link_index):
    if link_index >= len(LINKS):
        abort(404)
    if request.method == "POST":
        name = request.form["name"].strip()
        url = request.form["url"].strip()
        if not name or not url:
            abort(400)
        LINKS[link_index] = (name, url)
        return redirect(url_for("index"))
    name, url = LINKS[link_index]
    return render_template("edit.html", link_index=link_index, name=name, url=url)


@app.post("/delete/<int:link_index>")
def delete_link(link_index):
    if link_index >= len(LINKS):
        abort(404)
    LINKS.pop(link_index)
    return redirect(url_for("index"))


@app.get("/about")
def about():
    return render_template("about.html")
