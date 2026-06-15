# Aanchal Kataria — Resume Website

Personal resume site for Aanchal Kataria (Senior SDET / Test Automation Engineer).

## Live site

After GitHub Pages is enabled on the **AanchalKat** account, the site will be available at:

**https://aanchalkat.github.io/Aanchal-resume/**

> GitHub Pages may take 1–2 minutes to build after the first deploy.

## Local preview

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Regenerate PDF resume

```bash
python3 scripts/generate_resume_pdf.py
```

## Project structure

- `index.html` — main website
- `css/styles.css` — styles (light/dark theme)
- `js/main.js` — navigation and theme toggle
- `resume-pdf.html` — PDF layout source
- `assets/` — photo and downloadable resume PDF

## Publish to GitHub (AanchalKat on github.com)

Use **github.com only** (not GitHub Enterprise). Log in as **AanchalKat**, then from this folder:

```bash
export GH_HOST=github.com

gh auth login --hostname github.com --git-protocol ssh --web
gh auth switch --hostname github.com

git add .
git commit -m "Add personal resume website"

gh repo create Aanchal-resume \
  --private \
  --source=. \
  --remote=origin \
  --description "Personal resume website — Aanchal Kataria" \
  --push
```

Remote will be: `git@github.com:AanchalKat/Aanchal-resume.git`

Enable GitHub Pages: **Repository → Settings → Pages → Deploy from branch → `main` / `/ (root)`**.

## GitHub Pages

This is a static site. GitHub Pages serves `index.html` from the repository root on the `main` branch.
