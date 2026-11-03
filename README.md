# Codex_Flask_App
Practice from the LinkedIn training Codex App Deployment 

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run
```

The root URL (`/`) displays the My Links page.

Adding a link fetches its Open Graph title, description, and image URL. Missing
or empty tags and failed page requests display `Not Available`. Changing a link's
URL refreshes its metadata. Links and metadata are stored in memory and reset
when the app restarts; the initial example links use `Not Available` until their
URLs are changed.

## Error pages

Application-level 404 and 500 handlers render `templates/404.html` and
`templates/500.html` with the matching HTTP status. In debug mode, Flask's
interactive debugger handles unhandled exceptions instead of the 500 page.

The project includes a Context7 MCP configuration in `.codex/config.toml` using
`https://mcp.context7.com/mcp`. This chat retrieved Flask documentation directly
through that MCP endpoint; native tool availability depends on the host loading
the project configuration.

This environment's `codex mcp get context7` does not discover the project entry.
An explicit CLI override recognizes the server:

```sh
codex -c 'mcp_servers.context7.url="https://mcp.context7.com/mcp"' mcp get context7
```

References retrieved through Context7:

- [Flask stable documentation on Context7](https://context7.com/websites/flask_palletsprojects_en_stable)
- [Flask repository documentation on Context7](https://context7.com/pallets/flask)
- [Flask error handling](https://flask.palletsprojects.com/en/stable/errorhandling/)
- [Flask quickstart: errors](https://flask.palletsprojects.com/en/stable/quickstart/#redirects-and-errors)
- [Flask.errorhandler API](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.errorhandler)

Run the tests with `python -m unittest discover -s tests -v`.

## Styles

Tailwind CSS is compiled into `static/style.css` and served by Flask. Deployment
does not require Node.js. After changing Tailwind classes in the templates, rebuild
the stylesheet with Node.js and npm installed:

```sh
npm exec --yes --package=tailwindcss@3.4.17 -- tailwindcss -i ./static/tailwind.css -o ./static/style.css --content './templates/*.html' --minify
```
