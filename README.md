# Codex_Flask_App

## Project Overview

Practice from the LinkedIn training Codex App Deployment. This is a personal
link-in-bio application built with Python, Flask, Jinja templates, and Tailwind CSS.

## Features

The root URL (`/`) displays the My Links page.

- Add a site name and URL using the **Add Link** form.
- View rich link cards with a preview image, title, description, and clickable URL.
- Select **Edit** to change a link's name or URL, then **Save Changes** to return home.
- Select **Delete** to remove a link and return home.
- Select **Contact** in the homepage navigation to see a short message and a
  clickable email address. The page currently uses `contact@example.com`; replace
  it with your address in `templates/contact.html`.

Adding a link fetches its Open Graph title, description, and image URL. Missing
or empty tags and failed page requests display `Not Available`. Changing a link's
URL refreshes its metadata. Links and metadata are stored in memory and reset
when the app restarts; the initial example links use `Not Available` until their
URLs are changed.

### Routes

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Display the add form and link cards. |
| POST | `/add` | Submit `name` and `url` from the add form, fetch metadata, and redirect home. |
| GET | `/edit/<link_index>` | Open a pre-filled edit form from a card's Edit button. |
| POST | `/edit/<link_index>` | Submit `name` and `url`, update the link, and redirect home. |
| POST | `/delete/<link_index>` | Remove a link using its Delete button and redirect home. |
| GET | `/about` | Display the About page. |
| GET | `/contact` | Display the contact message and email address. |

Link indexes are zero-based positions in the current in-memory list.

### Error pages

Application-level 404 and 500 handlers render `templates/404.html` and
`templates/500.html` with the matching HTTP status. In debug mode, Flask's
interactive debugger handles unhandled exceptions instead of the 500 page.

References retrieved through Context7:

- [Flask stable documentation on Context7](https://context7.com/websites/flask_palletsprojects_en_stable)
- [Flask repository documentation on Context7](https://context7.com/pallets/flask)
- [Flask error handling](https://flask.palletsprojects.com/en/stable/errorhandling/)
- [Flask quickstart: errors](https://flask.palletsprojects.com/en/stable/quickstart/#redirects-and-errors)
- [Flask.errorhandler API](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.errorhandler)

## Setup

### Run locally

Use Python 3.10 or newer, as required by the pinned runtime dependencies.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run
```

Open `http://127.0.0.1:5000/` to use the app.

### Tests

```sh
.venv/bin/python -m unittest discover -s tests -v
```

### Deployment

`render.yaml` configures a free Python web service on Render with these commands:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`

### Context7 MCP

The project includes a Context7 MCP configuration in `.codex/config.toml` using
`https://mcp.context7.com/mcp`. Flask documentation was retrieved directly through
that MCP endpoint; native tool availability depends on the host loading the
project configuration.

This environment's `codex mcp get context7` does not discover the project entry.
An explicit CLI override recognizes the server:

```sh
codex -c 'mcp_servers.context7.url="https://mcp.context7.com/mcp"' mcp get context7
```

### Styles

Tailwind CSS is compiled into `static/style.css` and served by Flask. Deployment
does not require Node.js. After changing Tailwind classes in the templates, rebuild
the stylesheet with Node.js and npm installed:

```sh
npm exec --yes --package=tailwindcss@3.4.17 -- tailwindcss -i ./static/tailwind.css -o ./static/style.css --content './templates/*.html' --minify
```

### README maintenance

The `update-readme` skill is located at `.codex/skills/update-readme/SKILL.md`.
Ask Codex to use `$update-readme` after adding a feature, route, or dependency.

## Dependencies

Install the pinned Python packages with `pip install -r requirements.txt`:

| Package | Version | Purpose |
| --- | --- | --- |
| Flask | 3.1.2 | Web routes, templates, forms, static files, and error handling. |
| gunicorn | 26.2.0 | Production WSGI server. |
| requests | 2.34.2 | Fetch page HTML for link metadata. |
| beautifulsoup4 | 4.15.0 | Parse Open Graph tags from HTML. |

Tailwind CSS 3.4.17 is an optional build dependency run through npm. Node.js and
npm are needed only to rebuild the stylesheet, not to run or deploy the app.
Tests use Python's built-in `unittest` module and the runtime dependencies above.
