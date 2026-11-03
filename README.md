# Codex_Flask_App
Practice from the LinkedIn training Codex App Deployment 

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run
```

The root URL (`/`) displays the My Links page.

## Styles

Tailwind CSS is compiled into `static/style.css` and served by Flask. Deployment
does not require Node.js. After changing Tailwind classes in the templates, rebuild
the stylesheet with Node.js and npm installed:

```sh
npm exec --yes --package=tailwindcss@3.4.17 -- tailwindcss -i ./static/tailwind.css -o ./static/style.css --content './templates/*.html' --minify
```
