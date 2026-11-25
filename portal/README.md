# ONE Portal

The web view of the ACE One Management System. **Nothing in it is typed in by hand**: the build reads the Word documents in `finals/` and `manuals/`, the registers in `registers/`, the people list in `company/` and the rules in `protocol/`, and draws every page from them.

## Open it
- **On your computer:** open `portal/dist/index.html` (double-click). No server or installation is needed; everything is inside that one file.
- **Online:** https://oms.cynmark.app (once GitHub Pages and the domain are switched on — see below).

## How it stays up to date
Every time a document, register or portal file changes on `main`, the GitHub Action `.github/workflows/portal.yml` checks the documents against the ONE Protocol, rebuilds the portal and publishes it. Nobody edits the website.

## One-time setup for oms.cynmark.app
1. GitHub: repository **Settings > Pages > Build and deployment > Source: GitHub Actions**.
2. Your DNS provider for cynmark.app: add a **CNAME** record: name `oms`, value `scmwjtt.github.io`.
3. GitHub: **Settings > Pages > Custom domain**: `oms.cynmark.app`, then tick **Enforce HTTPS** when it becomes available.

## Pages
OMS wheel (with timeline) · Requirements explorer · Gaps · Risks (matrix with timeline, bow-tie per risk) · Controls · Technical authority · Library and reader · Processes (MOC swimlanes with the last 30 changes) · Performance · Search.

## Files
| Path | What it is |
|---|---|
| `src/index.html`, `src/style.css`, `src/app.js` | the portal source |
| `build/build.js` | reads the repository and writes `dist/` |
| `dist/index.html` | the built portal (self-contained) |
| `dist/one-data.json` | the data the portal draws from |

## Comments and suggested edits (v2)

Anyone viewing a document can point at a paragraph and add a comment or a suggested edit. Notes stay beside the document, never in it, until the owner acts:

1. The owner ticks "I am the document owner" (demo switch until staff sign-in exists) and accepts or rejects each edit.
2. "Download for Word" writes the accepted edits into the original Word file as tracked changes, with the author and date, and adds open comments as Word comments. Control ID fields are kept as they are.
3. The owner reviews in Word, issues the new revision and puts it in `finals/`. The site rebuilds itself.

All notes across all documents are listed under "Comments and edits" (`#/review`).

Notes are stored by the ONE API, a Cloudflare Worker with a D1 database at `https://oms-api.cynmark.app` (code in `worker/`, deployed by `.github/workflows/worker.yml`). If the API cannot be reached, the portal keeps notes in the browser and says so.
