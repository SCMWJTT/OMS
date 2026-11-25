# Moving ONE from an open GitHub demo to a company's SharePoint

Design note, 25 November 2026. This matters only when ONE is installed inside a client's network. Until then the public GitHub demo stays as it is.

## 1. The idea in one paragraph

The company's approved Word documents stay where they already live, in a SharePoint document library, with SharePoint managing versions, approvals and permissions. ONE becomes a **reading layer** on top: it reads the documents, builds the OMS view, and shows each person only what SharePoint already lets them open. Git keeps doing what it is good at: holding ONE's own code, the protocol, templates and the company's ONE configuration, and deploying new versions of the application. **Company documents never go into Git.**

## 2. Who does what

| Part | Today (demo) | Inside a company |
|---|---|---|
| Approved Word documents | `finals/` in a public GitHub repo | SharePoint document library (major versions = approved) |
| Drafts and reviews | `drafts/`, comments in the ONE API | SharePoint minor versions; ONE comments and suggested edits |
| Versions and approvals | Git history, pull requests | SharePoint versioning and its approval workflow (or Power Automate) |
| Permissions | none, everything public | SharePoint permissions and Microsoft Entra ID (Azure AD) groups |
| Staff, roles, functions | CSV files in `company/` | HR system or Entra ID (name, job title, manager), plus ONE's role and duty files |
| Registers (risk, controls, incidents, KPIs) | CSV files in `registers/` | SharePoint lists, or exports and connections from the systems the company already uses (risk tool, CMMS, incident system) |
| ONE application code, checker, templates, standard | public GitHub repo | the same code, deployed from a private repository (GitHub Enterprise or Azure DevOps) |
| Company's ONE configuration (codes, sites, element owners, role catalogue) | in the repo | private repository, or a SharePoint list |
| Web site | GitHub Pages, public | hosted inside the company's tenant (for example Azure Static Web Apps or App Service, or an internal server), behind company sign-in |
| Comments service | Cloudflare Worker, open | company database (for example Azure SQL or a SharePoint list), every entry tied to a signed-in person |

## 3. How it works

1. **Reading the library.** A small ONE service runs inside the company's tenant. It uses an app registration with access to the chosen site only (Microsoft Graph, "Sites.Selected" permission, approved by the tenant administrator). It reads each approved Word file, runs the same ONE checker and reader as today, and builds the index.
2. **Staying current.** SharePoint tells the service when a file changes (Graph change notifications, with a periodic "what changed since last time" check as a back-up). Only the changed documents are re-read. A new approved version appears in ONE within minutes; there is no build to run by hand.
3. **Signing in.** Users sign in with their normal company account (Microsoft Entra ID single sign-on). ONE learns their name, job title and groups.
4. **Showing only what you may see (security trimming).** For each document, the index records who may open it in SharePoint. When someone asks for a page, the service filters on the server and sends only what that person is allowed to see. Restricted content never reaches their browser.
5. **Drafts.** Drafts (SharePoint minor versions) are shown only to the people SharePoint lets see drafts: authors, reviewers and approvers.
6. **Comments and suggested edits.** Same as the demo, but every comment carries the person's real identity, and the comments live in the company's own database.
7. **Changing the Word document.** When the owner accepts suggested edits, ONE writes them into a new draft version of the real file in SharePoint as tracked changes, instead of a download. The owner finishes in Word or Word for the web, and SharePoint's approval publishes it. ONE then shows the new revision.

## 4. Decisions a company must make

- **What counts as published:** usually the latest major version with status Approved.
- **What ONE shows about hidden documents:** hide them completely, or show "3 restricted documents" so coverage counts stay honest. Counts and maps can reveal that something exists even when its text is hidden, so this must be a deliberate choice.
- **Where ONE runs:** company cloud tenant or an internal server; data residency.
- **Where staff data comes from:** HR system, Entra ID, or a maintained list.
- **Who may comment, and who may accept edits:** usually anyone with read access may comment, and only the document owner and Document Control may accept.

## 5. What has to change in ONE

| Area | Demo today | Needed for a company |
|---|---|---|
| Data delivery | all data built into one public web page | data served by an API, per user, after sign-in |
| Document source | files in `finals/` | SharePoint library through Microsoft Graph |
| Build trigger | GitHub Action on every push | change notifications from SharePoint; incremental re-indexing |
| Identity | anonymous name box, "I am the owner" switch | company sign-in; owner rights taken from the document's metadata and SharePoint permissions |
| Word download | browser builds a file to download | ONE writes a new draft version into SharePoint |
| Audit | none | log of who viewed, commented, accepted and published |
| Several sites or several OMSs | one company | one index per OMS, with comparisons across them |

The checker, the document reader, the OMS logic and all the views stay the same. That is the point of building them around the Word documents and not around a particular store.

## 6. Steps to get there

1. **Now:** public GitHub demo with fictional ACE data.
2. **Pilot, read only:** a copy of one library in a client tenant; ONE reads it, signs people in, shows everything to a small pilot group. Proves the reader and the gateway report on real documents.
3. **Security trimming:** per-user filtering, drafts limited to reviewers, decision on hidden documents.
4. **Comments with identities:** company database, audit log.
5. **Write-back and workflow:** accepted edits written into SharePoint drafts; approval workflow publishes; ONE republishes.
6. **More sources and sites:** registers from company systems; several sites and OMSs side by side.

## 7. What the client provides

- A SharePoint site and library for OMS documents, with versioning on.
- Administrator approval for ONE's app registration (access to that site only).
- The security groups that already control access.
- A place to host ONE, and a contact in IT security.
- Their documents, ideally converted to the ONE Document Standard. Documents that are not converted still appear, with their gateway findings, which is itself a useful first report.

## 8. Risks to plan for

- Microsoft Graph has rate limits; the first full read of a large library takes time and must be spread out.
- Permissions that are broken per file (unique permissions) are slower to read than library-wide ones.
- Documents not written to the standard give a thinner OMS view until they are converted.
- Search must also respect permissions: never index hidden text where everyone can search it.
