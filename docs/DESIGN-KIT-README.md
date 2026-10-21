# kubeAI Publications: magazine design, round 1

Design samples for the October 2026 issues of **SMB AI Accelerator** and **AI Business Advantage**, both "a kubeAI publication". This folder is the template for every later month and the reference for the team that builds the website or app.

Prepared 21 October 2026. Copy is placeholder (see "What is placeholder" below).

## What's in the folder

| Folder | Contents |
|---|---|
| `logos/` | Vector logos, type converted to outlines. kubeAI logo and cube mark, the "a kubeAI publication" endorsement (navy, white, indigo versions), and for each title: mark, horizontal lockup and cover masthead, positive and reverse. |
| `images/` | Original vector illustrations: `smb-cover`, `smb-feature`, `smb-hero` (navy ground for web), `aba-cover`, `aba-feature`. |
| `tokens/` | `brand.json` (colours, type, spacing, grid, focus, usage rules) and `tokens.css` (the same as CSS custom properties, scoped to `.t-smb` and `.t-aba`). |
| `fonts/` | Inter, Space Grotesk and Source Serif 4 (SIL Open Font Licence). Variable woff2 files plus `fonts.css` for the web; static TTF instances plus `fonts-print.css` for PDF. |
| `print/` | A4 page templates as HTML + `print.css`, and the rendered sample PDFs (7 pages each). |
| `web/` | Static web edition, one page per title, sharing `web.css`. No build step. |
| `email/` | 600px email edition per title, table layout with inline styles, plus `img/` (PNG/JPG only). |

## The two titles

| | SMB AI Accelerator | AI Business Advantage |
|---|---|---|
| Reader | Owners of small firms and their advisors | AI consultants and strategic advisors |
| Feel | Plain, energetic, practical | Strategic, premium, measured |
| Display face | Space Grotesk 700 | Source Serif 4 600, italic 400 for second clauses |
| Body face | Inter | Inter |
| Brand ground | Navy `#0B1F3A` | Indigo `#2E2A6B`, ink `#1B1840` |
| Accent | Orange `#F26B21` (fills, large type on navy) | Gold `#C9A227` (rules, numerals, type on indigo) |
| Accent as text | `#B4430E` on white (5.6:1) | `#7A5E10` on ivory (5.8:1) |
| Paper | White, warm `#FFF6EE` | Ivory `#FBF8F1` |
| Corners | 14px radius | Square |
| Print text | 2 columns | 3 columns |
| Illustration | Isometric clay world: small orange helpers working inside visible fences | Gold-on-indigo still lifes: scales, stairs, ledgers |

Shared: kubeAI navy and teal, the cube endorsement, Inter for reading, the 12-column grid, and the same component set.

**Colour rule.** The bright orange (3.0:1) and gold (2.4:1) fail WCAG AA as text on white. Use them only for fills, rules, icons, numerals and large type on dark grounds. On orange fills, text is navy, never white.

## Components

The same seven components exist in print (`print/print.css`) and web (`web/web.css`) with the same class names, so the Jinja2/WeasyPrint templates can share markup.

| Component | Class | Notes |
|---|---|---|
| Recommendations box | `.recs` (numbered `<ol>`) / `.recs.bold-lead` (ABA imperatives) | Tinted panel. SMB shows big numerals; ABA leads each item with a serif bold phrase. |
| Step-by-step blueprint | `.blueprint` with `.meta` and `ol.steps` | Numbered circles joined by a dashed line (squares for ABA). |
| Implications / Consultant Angle | `.angle` | SMB: orange left bar on warm paper. ABA: indigo panel, gold top rule, serif text. |
| Warning / always-review note | `.warn` (`.warn.privacy` for the teal privacy variant) | Icon + bold title + one or two sentences. `role="note"`. |
| Tool card | `.tool` with `.price` and `.caveat` | Name, what it does, price pill, caveat. Grid of up to 6. |
| Statistic call-out | `.stat` inside `.stats`; `.compare` for two-value gaps | Number, one-line label, source line. Every number keeps its source. |
| Sources list | `ol.sources` with `.sources-group` headings | Numbered 01, 02… grouped by section. Sources appear only here, no inline links. |

Also: `.signals` (Key signals from the inbox), `.deals` (VC & M&A list), `.bbpr` (build/buy/partner/redesign grid; mark the recommended cell `.pick`), `.bars` (simple cost chart with a budget line), `.pull` (pull quote), `.toc`, `.report-meta`.

**Chart style.** One per title. SMB: horizontal rounded bars, navy with orange highlights, dashed orange-text line for the budget threshold. ABA: flat indigo/gold bars, square ends, hairline gold source rule. Bars are drawn to one scale; labels are real text.

## Web edition (for the build team)

- Files: `web/smb-ai-accelerator-2026-10.html`, `web/ai-business-advantage-2026-10.html`, `web/web.css`. Theme by putting `t-smb` or `t-aba` on `<body>`.
- Layout: sticky site header, hero (title, standfirst, illustration), report-metadata strip, then article. At 1080px and up a sticky "In this issue" rail sits left of the article. Below that the contents become a boxed list above the article.
- Breakpoints: 360px minimum (checked, no horizontal scroll), 720px, 1080px. Content max width 1200px. Reading measure 68ch.
- Type: body 18px / 1.65. Headings use `clamp()` (h1 36–64px). Labels are uppercase with tracking.
- Accessibility: skip link, landmarks (`header`, `nav`, `main`, `footer`), one `h1`, ordered headings, alt text on every image, `aria-labelledby` on sections and components, visible 3px focus outline in the title's text-safe accent, `prefers-reduced-motion` respected, real text throughout.
- URLs and CTA destinations are `#` or `https://kubeai.info` until decided.

## PDF edition

- A4 portrait, 12-column grid, margins 18 / 16 / 22 / 18 mm (top / outside / bottom / inside), 5mm gutter.
- Pages: 1 cover, 2 contents + executive summary, 3–4 feature spread with recommendations and blueprints, 5 department page (SMB tools; ABA VC & M&A with build/buy/partner/redesign), 6 concluding remarks + sources, 7 back cover with kubeAI calls to action.
- Rendering: the HTML in `print/` is rendered with headless Chromium to a **tagged PDF** with a document outline and embedded TrueType subsets of the open fonts. It also works as a starting point for WeasyPrint: `@page { size: A4; margin: 0 }`, each `.page` is one sheet.

## Email edition

- 600px single column, tables + inline styles, works without the `<style>` block. Live text, PNG/JPG images only (no SVG), all images have width, height and alt text. Hidden preheader. Under 620px it goes full width.
- Sections: header with masthead and endorsement, lead headline + "Read the full issue" button, hero image, recommendations, a title-specific block (SMB blueprints + review warning; ABA stat row + Consultant Angle), product CTAs, footer with preferences and unsubscribe.
- Image paths are relative (`img/…`); host them on the sending platform and rewrite to absolute URLs before sending.

## What is placeholder

- **Copy.** The October outline v2 files were not available, so body copy is written around the leads named in the brief ("Your first agent is already inside your software, so set its limits"; "The Distrust Tax: pricing oversight and data readiness"). Every print page is marked "Design sample · placeholder copy". Swap in the final issue text (compiled 25–28 October).
- **Figures.** Only numbers quoted in the brief are shown (31%, 45%, 46%, 64% vs 9%). Their labels and sources are visible empty slots, so no figure is invented.
- **Tools.** SMB tool names and prices are empty slots; the cost chart bars are illustrative.
- **CTAs.** Product one-liners for 12 Play Testers and ScrollRSI, and all destination URLs.
- **Address** in the email footer.

## Imagery note

Canva's image generator produced four concept images (in Yacine's Canva account) before its credit quota ran out, and this environment could not download the full-size files. The illustrations used here are original vector artwork drawn in the same style, so they scale to any size and can be recoloured or recomposed for later issues.
