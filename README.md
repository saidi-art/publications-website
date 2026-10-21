# kubeAI Publications website

Static site for the two kubeAI monthly magazines, **SMB AI Accelerator** and
**AI Business Advantage**, both "a kubeAI publication". Built from the round-1
design kit (see `docs/DESIGN-KIT-README.md`).

- Proposed address: `publications.kubeai.info` (CNAME included). HTTPS is
  enforced by GitHub Pages from day one. Yacine confirms the final address.
- Nothing goes live until Yacine approves. GitHub Pages and the DNS record are
  deliberately NOT enabled yet.

## Structure

- `index.html` — publications home: both titles, subscribe call to action.
- `<slug>/index.html` — landing page per title: latest issue + archive.
- `<slug>/<yyyy-mm>/index.html` — one page per issue (web edition).
- `<slug>/<yyyy-mm>/<slug>-<yyyy-mm>.pdf` — PDF edition, next to the page.
- `subscribe/`, `privacy/`, `contact/`, `404.html`, `robots.txt`, `sitemap.xml`,
  `feeds/<slug>.xml` (one RSS feed per title).
- `assets/css/`, `assets/fonts/` — **slots** for the kit's `tokens.css`,
  `web.css` and self-hosted woff2 fonts (`font-display: swap`). The kit's web
  files were not in the round-1 handoff; nothing here restyles them.
- `templates/build.py` — renders every page. No build step beyond running it.

## Content comes from data

Issue copy lives only in `data/issues/<slug>-<yyyy-mm>.json`, produced by the
production pipeline (Paperclip). After Yacine approves the PDF:

1. Drop the issue JSON into `data/issues/`.
2. `python3 templates/build.py`.
3. Commit and push. Corrections go back through the pipeline; issue text is
   never edited on the site.

The schema is documented by `data/issues/issue.example.json` (placeholder).

## Calls to action

Every outbound link carries
`utm_source=kubeai-publications&utm_medium=web&utm_campaign=<title>-<yyyy-mm>`
(`publications-home` on non-issue pages).

- Subscribe: main call to action on every page. The MailerLite embed
  (double opt-in) replaces the marked `SUBSCRIBE SLOT` block in
  `subscribe/index.html` and the home page once the account exists.
- ScrollRSI waitlist: https://scrollrsi.kubeai.info (fits SMB AI Accelerator best)
- 12 Play Testers: https://play.kubeai.info/
- Work with kubeAI: https://kubeai.info (until a services/contact page exists)

## Privacy

No cookies, no third-party trackers. The signup privacy line mirrors the
ScrollRSI site. Analytics slot is reserved for a cookieless option (Plausible
or Cloudflare Web Analytics) once chosen.

## Pending from the round-1 kit

- `tokens/tokens.css`, `tokens/brand.json`
- `web/web.css` and both web edition pages (`smb-ai-accelerator-2026-10.html`,
  `ai-business-advantage-2026-10.html`)
- `fonts/` (variable woff2 + `fonts.css`)
- vector logos, cube mark (for the favicon), and the original illustrations
- the SMB email template (`email/smb-ai-accelerator-2026-10.html`)
- `print/` templates

What arrived in the handoff: the kit README, the ABA email edition, the ABA
hero JPG, the reverse logo/endorsement PNGs, and both 7-page sample PDFs.
