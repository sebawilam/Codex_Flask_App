import requests
from bs4 import BeautifulSoup
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


DEFAULT_METADATA = {
    "title": "Not Available",
    "description": "Not Available",
    "image_url": "Not Available",
}

LINKS = [
    {"name": name, "url": url, **DEFAULT_METADATA}
    for name, url in [
        ("Python", "https://www.python.org/"),
        ("Flask", "https://flask.palletsprojects.com/"),
        ("GitHub", "https://github.com/"),
    ]
]


def fetch_metadata(url):
    metadata = DEFAULT_METADATA.copy()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return metadata

    soup = BeautifulSoup(response.content, "html.parser")
    for field, property_name in [
        ("title", "og:title"),
        ("description", "og:description"),
        ("image_url", "og:image"),
    ]:
        tag = soup.find("meta", attrs={"property": property_name})
        if tag:
            content = tag.get("content", "").strip()
            if content:
                metadata[field] = content
    return metadata


@app.get("/")
def index():
    return render_template("index.html", links=LINKS)


@app.post("/add")
def add_link():
    name = request.form["name"].strip()
    url = request.form["url"].strip()
    if not name or not url:
        abort(400)
    LINKS.append({"name": name, "url": url, **fetch_metadata(url)})
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
        link = LINKS[link_index].copy()
        if url != link["url"]:
            link.update(fetch_metadata(url))
        link.update(name=name, url=url)
        LINKS[link_index] = link
        return redirect(url_for("index"))
    link = LINKS[link_index]
    return render_template(
        "edit.html", link_index=link_index, name=link["name"], url=link["url"]
    )


@app.post("/delete/<int:link_index>")
def delete_link(link_index):
    if link_index >= len(LINKS):
        abort(404)
    LINKS.pop(link_index)
    return redirect(url_for("index"))


@app.get("/about")
def about():
    return render_template("about.html")


@app.get("/contact")
def contact():
    return render_template("contact.html")
