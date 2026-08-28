# Research Project Template

This repository is a **minimal template for research and data science projects** that combine code, documentation, and a project website.

It includes:

* a clean project structure (`src`, `data`, `docs`, `tests`, etc.)
* a documentation website built with **MkDocs + Material**
* automatic deployment to **GitHub Pages** using GitHub Actions
* development history files (changelog, roadmap, dev log)
* an `AGENTS.md` file with guidance for AI coding agents

The website is built from the `docs/` folder and automatically deployed when changes are pushed.

---

# Enable the Website

After creating a repository from this template you must enable GitHub Pages once.

1. Go to **Settings → Pages**
2. Under **Build and deployment**, choose
   **Source: GitHub Actions**

The site will then deploy automatically on push.

Your site will appear at:

```
https://<your-username>.github.io/<repository-name>/
```

---

# Preview Locally

```
pip install mkdocs mkdocs-material
mkdocs serve
```

Then open:

```
http://127.0.0.1:8000
```

---

Use **"Use this template"** on GitHub to start a new project.
