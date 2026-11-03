---
name: update-readme
description: Update README.md for this Flask project when setup, routes, features, dependencies, tests, or deployment instructions change.
---

# Update the README

1. Read `AGENTS.md`, the current `README.md`, and the relevant project files before editing documentation.
2. Check `app.py`, `templates/`, `static/`, `requirements.txt`, `tests/`, and `render.yaml` as needed to verify behavior and commands.
3. Update only the README sections affected by the requested change. Preserve useful existing content and keep instructions concise.
4. Document local setup using a virtual environment and `python -m pip install -r requirements.txt`. Start the app with `python -m flask --app app run` using that environment's Python.
5. Describe actual routes, features, data persistence, and limitations supported by the code. Do not invent configuration, features, or deployment steps.
6. If documenting tests, verify the command against the project; the existing unittest suite runs with `python -m unittest discover -s tests`.
7. When Flask API details need clarification, consult the Context7 MCP server if available and use documentation matching the installed Flask version.
8. Check referenced paths and commands. Report which README sections changed, what was verified, and any checks that could not run.
