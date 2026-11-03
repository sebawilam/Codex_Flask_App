---
name: update-readme
description: Use this skill when a new feature, route, or dependency is added to the project.
---

# Update README

Keep the project README accurate after implementing a change.

## Instructions

1. Read the project's `AGENTS.md`, the current `README.md`, and the relevant code
   changes. Inspect routes, templates, `requirements.txt`, and deployment files as
   needed to confirm the actual behavior and dependencies.
2. Update `README.md` with a concise description of what changed and how to use
   each new feature. For a new route, include its HTTP method, path, purpose, and
   how a user accesses it or submits data to it.
3. Document any new dependencies, their purpose, and installation or build steps.
   Copy versions from the dependency manifest; do not guess versions or claim a
   dependency was added if it was already present.
4. Keep the README organized with these sections:
   - `Project Overview`: the project's purpose and technology.
   - `Features`: supported functionality, routes, and relevant limitations.
   - `Setup`: installation, local startup, tests, and deployment or styling steps.
   - `Dependencies`: runtime packages and optional development or build tools.
5. Follow the existing README format if one exists, preserving its project title,
   Markdown conventions, useful examples, and accurate information. Fit existing
   material under the four sections using subsections where helpful. If no README
   exists, create one with the four sections.
6. Verify commands, file paths, route methods, and dependency names against the
   project. Remove outdated or duplicate instructions and run `git diff --check`.
   Do not change application code or add dependencies solely to update the README.
7. Report which README sections changed and any information you could not verify.

## Invocation

When this skill is available, invoke it with `$update-readme` or ask Codex to use
the `update-readme` skill. This is an instruction-based skill: Codex executes it by
reading this file and following the workflow; no executable script is required.
