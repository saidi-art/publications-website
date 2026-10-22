#!/usr/bin/env python3
"""kubeAI Publications static site builder.

Renders every page from data + templates in this folder. No build step beyond
running this script. Issue copy lives ONLY in data/issues/*.json; the website
never carries hand-edited issue text (corrections go back through the pipeline).

Usage:  python3 templates/build.py   (run from the repository root)
"""
import json, os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "https://publications.kubeai.info"   # proposed address; Yacine confirms the final one
BRAND = "kubeAI Publications"
CONTACT_EMAIL = "saidi@kubeai.info"
SERVICES_URL = "https://kubeai.info"
PLAY_URL = "https://play.kubeai.info/"
SCROLLRSI_URL = "https://scrollrsi.kubeai.info"

TITLES = {
    "smb-ai-accelerator": {
        "name": "SMB AI Accelerator",
        "theme": "t-smb",
        "strapline": "Practical AI for owners of small firms and their advisors.",
        "feed_desc": "Practical AI for owners of small firms and their advisors. A kubeAI publication.",
        "meta_desc": "SMB AI Accelerator, a free monthly magazine from kubeAI: plain, practical AI steps for owners of small firms and their advisors.",
    },
    "ai-business-advantage": {
        "name": "AI Business Advantage",
        "theme": "t-aba",
        "strapline": "Strategic AI analysis for AI consultants and strategic advisors.",
        "feed_desc": "Strategic AI analysis for AI consultants and strategic advisors. A kubeAI publication.",
        "meta_desc": "AI Business Advantage, a free monthly magazine from kubeAI: strategic AI research, deal flow and governance for consultants and advisors.",
    },
}

# ---------------------------------------------------------------------------
# October 2026 placeholder issues. REPLACE via the production pipeline: drop
# data/issues/<slug>-<yyyy-mm>.json (compiled 25-28 Oct) and rerun this script.
# ---------------------------------------------------------------------------
ISSUES = {
    "smb-ai-accelerator-2026-10": {
        "title": "smb-ai-accelerator", "volume": "2026-10",
        "report_date": "2026-10-28", "period": "October 2026",
        "kicker": "Monthly Intelligence Report · October 2026 · Free",
        "focus": "Agents inside everyday software",
        "headline_main": "Your first agent is already inside your software,",
        "headline_italic": "so set its limits.",
        "standfirst": "PLACEHOLDER COPY from the round-1 design sample. The real standfirst arrives with the October issue data from the pipeline.",
        "hero": {"src": None, "alt": ""},
        "og_image": None, "pdf_published": False,
        "sections": [],   # empty until the October issue.json lands
        "placeholder": True,
    },
    "ai-business-advantage-2026-10": {
        "title": "ai-business-advantage", "volume": "2026-10",
        "report_date": "2026-10-28", "period": "October 2026",
        "kicker": "Monthly Intelligence Report · October 2026",
        "focus": "Strategic research & foundational shifts",
        "headline_main": "The Distrust Tax:",
        "headline_italic": "pricing oversight and data readiness.",
        "standfirst": "PLACEHOLDER COPY from the round-1 design sample. The real standfirst arrives with the October issue data from the pipeline.",
        "hero": {"src": "/assets/img/aba-hero.jpg", "alt": "An indigo staircase rises to the right, each step edged in gold; one step is repaired with gold."},
        "og_image": "/assets/img/aba-hero.jpg", "pdf_published": False,
        "sections": [],
        "placeholder": True,
    },
}
# Real issue data overrides the built-in placeholders when present (production path).
_data_dir = os.path.join(ROOT, "data", "issues")
if os.path.isdir(_data_dir):
    for fn in sorted(os.listdir(_data_dir)):
        if fn.endswith(".json") and not fn.endswith(".example.json"):
            with open(os.path.join(_data_dir, fn), encoding="utf-8") as fh:
                d = json.load(fh)
            ISSUES[f"{d['title']}-{d['volume']}"] = d

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def utm(url, campaign):
    """Tag every outbound link per the site brief."""
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source=kubeai-publications&utm_medium=web&utm_campaign={campaign}"

def w(path, text):
    path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote", path)

def campaign_for(slug_or_none):
    if slug_or_none:
        iss = latest_issue(slug_or_none)
        return f"{slug_or_none}-{iss['volume']}"
    return "publications-home"

# MailerLite Universal snippet: powers the embedded subscribe form on every page.
# Plain string on purpose: the JS braces must not sit inside an f-string.
# Keeps the MailerLite success message clear of the sticky header when the browser scrolls to it.
ML_SCROLL_FIX = "<style>.ml-embedded,.subscribe-slot,#subscribe{scroll-margin-top:88px}</style>"

ML_HEAD = """<script>
(function(w,d,e,u,f,l,n){w[f]=w[f]||function(){(w[f].q=w[f].q||[]).push(arguments);},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);})(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');ml('account','2732749');
</script>
"""

def head(title, desc, canonical, og_image=None, og_type="website"):
    ogi = og_image or "/assets/img/aba-hero.jpg"
    ogu = SITE + ogi
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ogu}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{ogu}">
<meta name="color-scheme" content="light">
<!-- ANALYTICS SLOT: privacy-friendly, cookieless analytics only (Plausible or Cloudflare Web Analytics). No third-party trackers. -->
<link rel="icon" type="image/png" href="/assets/logos/kubeai-logo-reverse.png">
<link rel="apple-touch-icon" href="/assets/logos/kubeai-logo-reverse.png">
<link rel="stylesheet" href="/assets/css/web.css">
{ML_SCROLL_FIX}
{ML_HEAD}
</head>"""

def chrome(body_html, body_class="t-aba", title="", desc="", canonical="", og_image=None, og_type="website", campaign="publications-home", logo="/assets/logos/kubeai-logo-reverse.svg", logo_alt="kubeAI Publications", wrap="prose"):
    h = head(title, desc, canonical, og_image=og_image, og_type=og_type)
    nav = f"""
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="container">
    <a class="logo" href="/" aria-label="kubeAI Publications home"><img src="{logo}" alt="{esc(logo_alt)}"></a>
    <nav aria-label="Site">
      <ul>
        <li><a href="/" {"aria-current='page'" if canonical == SITE + "/" else ""}>Magazines</a></li>
        <li><a href="/smb-ai-accelerator/" {"aria-current='page'" if canonical == SITE + "/smb-ai-accelerator/" else ""}>SMB AI Accelerator</a></li>
        <li><a href="/ai-business-advantage/" {"aria-current='page'" if canonical == SITE + "/ai-business-advantage/" else ""}>AI Business Advantage</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a class="subscribe" href="{utm(SITE + '/subscribe/', campaign)}">Subscribe free</a></li>
      </ul>
    </nav>
  </div>
</header>"""
    footer = f"""
<footer class="site-foot">
  <div class="container">
    <img src="/assets/logos/kubeai-logo-reverse.svg" alt="kubeAI">
    <p>kubeAI publishes two free monthly magazines. <a href="/privacy/">Privacy</a> &middot; <a href="/contact/">Contact</a> &middot; <a href="{utm(SERVICES_URL, campaign)}">kubeai.info</a></p>
    <p>RSS: <a href="/feeds/smb-ai-accelerator.xml">SMB AI Accelerator</a> &middot; <a href="/feeds/ai-business-advantage.xml">AI Business Advantage</a></p>
    <p>&copy; 2026 KubeAI. Both magazines are free, every month.</p>
  </div>
</footer>"""
    if wrap == "prose":
        inner = f'<main id="main">\n<div class="container">\n<div class="prose">\n{body_html}\n</div>\n</div>\n</main>'
    else:
        inner = body_html
    return f"""{h}
<body class="{body_class}">
{nav}
{inner}
{footer}
</body>
</html>"""

def latest_issue(slug):
    ks = [k for k, v in sorted(ISSUES.items()) if v["title"] == slug]
    return ISSUES[ks[-1]]

def issues_for(slug):
    return [ISSUES[k] for k in sorted(ISSUES) if ISSUES[k]["title"] == slug]

def issue_url(iss): return f"/{iss['title']}/{iss['volume']}/"
def issue_pdf(iss): return f"/{iss['title']}/{iss['volume']}/{iss['title']}-{iss['volume']}.pdf"
def period_name(iss): return datetime.strptime(iss["volume"], "%Y-%m").strftime("%B %Y")
def next_period(iss):
    y, m = map(int, iss["volume"].split("-"))
    y += (m == 12); m = m % 12 + 1
    return datetime(y, m, 1).strftime("%B %Y")

# --- subscribe slot (MailerLite embed replaces this block; double opt-in) ---
SUBSCRIBE_SLOT = """
<div class="subscribe-slot">
  <!-- MailerLite embedded form: kubeAI Publications subscribe (double opt-in) -->
  <div class="ml-embedded" data-form="LF22mS"></div>
</div>"""

PRIVACY_LINE = ('<p class="privacy-line">When you subscribe, we store your email address and the '
 "time you joined, nothing else. We use it only to send you the magazines you asked for. Each "
 f"subscription is confirmed with a double opt-in email, and you can unsubscribe from any issue. "
 f"Removing your address: write to {CONTACT_EMAIL} and we will delete it.</p>")

PRODUCTS = [
    ("ScrollRSI", SCROLLRSI_URL, "Turn any scrolling screen into a clean text file, right on your phone."),
    ("12 Play Testers", PLAY_URL, "A human-in-the-loop QA crew for agents that ship Android apps."),
    ("Work with kubeAI", SERVICES_URL, "Advisory support for governance and data readiness."),
]

def product_links(campaign):
    items = "\n".join(
        f'<li><a href="{utm(url, campaign)}"><strong>{esc(name)}</strong></a><br>{esc(line)}</li>'
        for name, url, line in PRODUCTS)
    return f'<ul class="product-links">\n{items}\n</ul>'

# --- page bodies ------------------------------------------------------------
def home():
    cards = "\n".join(f"""
  <section class="title-card" aria-labelledby="h-{slug}">
    <h2 id="h-{slug}"><a href="/{slug}/">{esc(t['name'])}</a></h2>
    <p>{esc(t['strapline'])}</p>
    <p class="latest">Latest issue: <a href="{issue_url(latest_issue(slug))}">{esc(period_name(latest_issue(slug)))}</a></p>
  </section>""" for slug, t in TITLES.items())
    body = f"""
<h1>Two monthly magazines, a kubeAI publication</h1>
<p>kubeAI publishes two free monthly magazines. SMB AI Accelerator is the plain, practical read
for owners of small firms and their advisors. AI Business Advantage is the strategic read for AI
consultants. Both arrive monthly, free, and every figure is sourced.</p>
<p><a class="cta" href="{utm(SITE + '/subscribe/', 'publications-home')}">Subscribe free</a></p>
{cards}
<section aria-labelledby="h-products">
  <h2 id="h-products">From kubeAI</h2>
  {product_links('publications-home')}
</section>"""
    return chrome(body, title=f"{BRAND}: two monthly magazines", desc="kubeAI publishes two free monthly AI magazines: SMB AI Accelerator for small firms, AI Business Advantage for consultants. Subscribe free.", canonical=SITE + "/")

def landing(slug):
    t = TITLES[slug]; iss = latest_issue(slug)
    camp = campaign_for(slug)
    pdf_btn = (f'<p><a class="cta" href="{issue_pdf(iss)}">Download the PDF edition</a></p>'
               if iss.get("pdf_published") else
               '<p class="pending">The PDF edition arrives once the October issue is approved.</p>')
    archive = "\n".join(
        f'<li><a href="{issue_url(i)}">{esc(period_name(i))}</a>'
        + (f' · <a href="{issue_pdf(i)}">PDF</a>' if i.get("pdf_published") else "") + "</li>"
        for i in reversed(issues_for(slug)))
    body = f"""
<h1>{esc(t['name'])}</h1>
<p class="strapline">{esc(t['strapline'])}</p>
<p><a class="cta" href="{utm(SITE + '/subscribe/', camp)}">Subscribe free</a></p>
<section aria-labelledby="h-latest">
  <h2 id="h-latest">Latest issue</h2>
  <p><a href="{issue_url(iss)}">{esc(period_name(iss))} · {esc(iss['headline_main'] + ' ' + iss['headline_italic'])}</a></p>
  {pdf_btn}
</section>
<section aria-labelledby="h-archive">
  <h2 id="h-archive">Archive</h2>
  <ol>
{archive}
  </ol>
</section>
<section aria-labelledby="h-products-{slug}">
  <h2 id="h-products-{slug}">From kubeAI</h2>
  {product_links(camp)}
</section>"""
    return chrome(body, body_class=t["theme"], title=f"{t['name']} · {BRAND}", desc=t["meta_desc"], canonical=f"{SITE}/{slug}/", campaign=camp)

def issue_page(iss):
    slug = iss["title"]; t = TITLES[slug]
    camp = campaign_for(slug)
    url = SITE + issue_url(iss)
    img = iss.get("og_image") or None
    pdf = (f'<p><a class="cta" href="{issue_pdf(iss)}">Download the PDF edition</a></p>'
           if iss.get("pdf_published") else
           '<p class="pending">The PDF edition lands here once the issue is approved.</p>')
    sections = "\n".join(render_section(s, iss) for s in iss.get("sections", []))
    endorse = "endorsement-reverse.svg" if slug == "smb-ai-accelerator" else "endorsement-aba.svg"
    if iss.get("hero", {}).get("src"):
        hi = iss["hero"]
        hero_fig = f'  <figure><img src="{hi["src"]}" alt="{esc(hi["alt"])}" width="1200" height="668" loading="lazy"></figure>'
    else:
        cover = "smb-cover.svg" if slug == "smb-ai-accelerator" else "aba-cover.svg"
        hero_fig = f'  <figure><img src="/assets/img/{cover}" width="1800" height="1000" alt="Cover art for {esc(t["name"])}, {esc(period_name(iss))}" loading="lazy"></figure>'
    has_sources = any(s.get("component") == "sources" for s in iss.get("sections", []))
    toc = "\n".join(f'<li><a href="#s-{s["id"]}">{esc(s["heading"])}</a></li>' for s in iss.get("sections", []))
    if has_sources:
        toc += '\n<li><a href="#sources">Sources</a></li>'
    cta_cards = "\n      ".join(
        f'<a href="{utm(u, camp)}"><b>{esc(n)}</b><span>{esc(l)}</span><i>Learn more &rarr;</i></a>'
        for n, u, l in PRODUCTS)
    placeholder = ('\n    <p class="sample-note">Design sample &middot; placeholder copy. The October issue copy is '
        'compiled 25 to 28 October and will replace this page from the production pipeline. Issue text is '
        'never edited on the site.</p>') if iss.get("placeholder") else ""
    body = f"""
<div class="hero">
  <div class="container">
    <div class="copy">
      <p class="endorse"><img src="/assets/logos/{endorse}" alt="a kubeAI publication"></p>
      <p class="kicker">{esc(iss['kicker'])}</p>
      <h1>{esc(iss['headline_main'])} <em>{esc(iss['headline_italic'])}</em></h1>
      <p class="standfirst">{esc(iss['standfirst'])}</p>
    </div>
{hero_fig}
  </div>
</div>
<div class="report-meta">
  <div class="container">
    <dl>
      <div><dt>Report date</dt><dd>{esc(iss['report_date'])}</dd></div>
      <div><dt>Reporting period</dt><dd>{esc(iss['period'])}</dd></div>
      <div><dt>Focus</dt><dd>{esc(iss.get('focus',''))}</dd></div>
    </dl>
  </div>
</div>
<div class="container layout">
  <nav class="toc" aria-labelledby="toc-h">
    <h2 id="toc-h">In this issue</h2>
    <ol>
      {toc}
    </ol>
  </nav>
  <main id="main">
    <article class="article">{placeholder}
{sections}
    </article>
  </main>
</div>
<div class="container">
  {pdf}
</div>
<section class="cta-band" id="subscribe" aria-labelledby="cta-h">
  <div class="container">
    <h2 id="cta-h">Put this issue to work <em>this week.</em></h2>
    <div class="cta-grid">
      {cta_cards}
    </div>
  </div>
</section>"""
    return chrome(body, body_class=t["theme"], title=f"{t['name']} · {period_name(iss)}", desc=t["meta_desc"], canonical=url, og_image=img, og_type="article", campaign=camp, wrap=None)

def render_section(s, iss):
    c = s.get("component"); sid = s["id"]
    if c == "article":
        return f'<section aria-labelledby="s-{sid}">\n<div class="section-head"><h2 id="s-{sid}">{esc(s["heading"])}</h2></div>\n<div class="prose">\n{s["body_html"]}\n</div>\n</section>'
    if c == "recs":
        items = "".join(f"<li>{r['html']}</li>" for r in s["items"])
        cls = "recs bold-lead" if s.get("bold_lead") else "recs"
        return f'<section class="{cls}" aria-labelledby="s-{sid}">\n<h2 id="s-{sid}">{esc(s["heading"])}</h2>\n<ol>{items}</ol>\n</section>'
    if c == "blueprint":
        steps = "".join(f"<li>{st['html']}</li>" for st in s["steps"])
        meta = "".join(f"<li>{esc(m)}</li>" for m in s.get("meta", []))
        return (f'<section class="stack" aria-labelledby="s-{sid}">\n<div class="blueprints">\n<article class="blueprint" aria-labelledby="s-{sid}">\n<h3 id="s-{sid}">{esc(s["heading"])}</h3>\n<ul class="meta">{meta}</ul>\n<ol class="steps">{steps}</ol>\n</article>\n</div>\n</section>')
    if c == "angle":
        return f'<aside class="angle" aria-labelledby="s-{sid}">\n<p class="label" id="s-{sid}">{esc(s["heading"])}</p>\n<p>{s["html"]}</p>\n</aside>'
    if c == "warn":
        cls = "warn privacy" if s.get("variant") == "privacy" else "warn"
        svg = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 23 21H1z" fill="var(--accent)"/>'
               '<path d="M12 9v5" stroke="var(--on-accent)" stroke-width="2.4" stroke-linecap="round"/>'
               '<circle cx="12" cy="17.3" r="1.4" fill="var(--on-accent)"/></svg>')
        return f'<div class="{cls}" role="note" aria-labelledby="s-{sid}">\n{svg}\n<p><strong id="s-{sid}">{esc(s["heading"])}</strong>{esc(s["text"])}</p>\n</div>'
    if c == "tools":
        cards = "".join(
            f'<article class="tool"><p class="label">{esc(tl["category"])}</p><h3>{esc(tl["name"])}</h3><p>{esc(tl["what"])}</p><p class="price">{esc(tl["price"])}</p><p class="caveat">Caveat · {esc(tl["caveat"])}</p></article>'
            for tl in s["tools"])
        return f'<section aria-labelledby="s-{sid}">\n<h2 id="s-{sid}">{esc(s["heading"])}</h2>\n<div class="tools">{cards}</div>\n</section>'
    if c == "stats":
        stats = "".join(
            f'<div class="stat"><p class="n">{esc(st["n"])}</p><p class="label">{esc(st["label"])}</p><p class="source">Source · {esc(st["source"])}</p></div>'
            for st in s["stats"])
        return f'<section class="stats" aria-labelledby="s-{sid}">\n<h2 id="s-{sid}">{esc(s["heading"])}</h2>\n{stats}\n</section>'
    if c == "compare":
        return (f'<section class="compare" aria-labelledby="s-{sid}">\n<h2 id="s-{sid}">{esc(s["heading"])}</h2>\n'
                f'<div class="stat"><p class="n">{esc(s["a"]["n"])}</p><p class="label">{esc(s["a"]["label"])}</p></div>'
                f'<div class="stat"><p class="n">{esc(s["b"]["n"])}</p><p class="label">{esc(s["b"]["label"])}</p></div>'
                f'<p class="source">Source · {esc(s["source"])}</p>\n</section>')
    if c == "sources":
        groups = ""
        for g in s["groups"]:
            lis = "".join(f'<li><span class="src-n">{i:02d}</span> {it["html"]}</li>' for i, it in zip(range(g["start"], g["start"] + len(g["items"])), g["items"]))
            groups += f'<div class="sources-group"><h3>{esc(g["heading"])}</h3><ol class="sources" start="{g["start"]}">{lis}</ol></div>'
        return f'<section aria-labelledby="s-{sid}">\n<h2 id="s-{sid}">{esc(s["heading"])}</h2>\n{groups}\n</section>'
    raise SystemExit(f"Unknown component {c!r} in {iss['title']}-{iss['volume']}")

def subscribe():
    body = f"""
<h1>Subscribe</h1>
<p>Both magazines are free, every month. Pick your titles, confirm the double opt-in email,
and the next issue lands in your inbox.</p>
{SUBSCRIBE_SLOT}
{PRIVACY_LINE}"""
    return chrome(body, title=f"Subscribe · {BRAND}", desc="Subscribe free to SMB AI Accelerator and AI Business Advantage, the two monthly magazines from kubeAI.", canonical=SITE + "/subscribe/", og_image="/assets/img/aba-hero.jpg")

def privacy():
    body = f"""
<h1>Privacy policy</h1>
<p>This site does not use cookies, advertising trackers or third-party trackers. If we add
privacy-friendly analytics, which works without cookies, this page will say so before it goes live.</p>
<h2>The magazines</h2>
<p>When you subscribe, we store your email address and the time you joined, nothing else. We use it
only to send you the magazines you asked for. Every subscription is confirmed with a double opt-in
email, and every issue carries an unsubscribe link.</p>
<h2>Removing your address</h2>
<p>Write to {CONTACT_EMAIL} and we will delete it.</p>
<p><a href="/">Back to {esc(BRAND)}</a></p>"""
    return chrome(body, title=f"Privacy · {BRAND}", desc="Privacy policy for publications.kubeai.info: no cookies, no trackers, email used only to send the magazines you asked for.", canonical=SITE + "/privacy/", og_image="/assets/img/aba-hero.jpg")

def contact():
    body = f"""
<h1>Contact</h1>
<p>Questions about the magazines, corrections or story ideas: write to <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
<p>Corrections to a published issue go back through the production pipeline; we never edit issue
text on the site.</p>
<p>For everything else kubeAI does, see <a href="{utm(SERVICES_URL, 'publications-home')}">kubeai.info</a>.</p>"""
    return chrome(body, title=f"Contact · {BRAND}", desc="Contact kubeAI Publications: questions, corrections and story ideas.", canonical=SITE + "/contact/", og_image="/assets/img/aba-hero.jpg")

def notfound():
    body = '<h1>Page not found</h1>\n<p><a href="/">Back to the publications home page</a></p>'
    return chrome(body, title=f"Page not found · {BRAND}", desc="Page not found.", canonical=SITE + "/404.html", og_image="/assets/img/aba-hero.jpg")

def feeds():
    for slug, t in TITLES.items():
        items = ""
        for iss in reversed(issues_for(slug)):
            d = datetime.strptime(iss["report_date"], "%Y-%m-%d").replace(hour=9, tzinfo=timezone.utc)
            items += (f"<item><title>{esc(t['name'] + ' · ' + period_name(iss))}</title>"
                      f"<link>{SITE}{issue_url(iss)}</link>"
                      f'<guid isPermaLink="true">{SITE}{issue_url(iss)}</guid>'
                      f"<pubDate>{d.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>"
                      f"<description>{esc(iss['headline_main'] + ' ' + iss['headline_italic'])}</description></item>")
        w(f"feeds/{slug}.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="/feeds/feed.xsl" type="text/xsl"?>
<rss version="2.0"><channel>
<title>{esc(t['name'])}</title>
<link>{SITE}/{slug}/</link>
<description>{esc(t['feed_desc'])}</description>
<language>en-gb</language>
{items}
</channel></rss>
""")

def sitemap():
    urls = ["/", "/subscribe/", "/privacy/", "/contact/"] + [f"/{slug}/" for slug in TITLES]
    for iss in ISSUES.values():
        urls.append(issue_url(iss))
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")

def main():
    w("index.html", home())
    w("subscribe/index.html", subscribe())
    w("privacy/index.html", privacy())
    w("contact/index.html", contact())
    w("404.html", notfound())
    for slug in TITLES:
        w(f"{slug}/index.html", landing(slug))
    for iss in ISSUES.values():
        w(f"{iss['title']}/{iss['volume']}/index.html", issue_page(iss))
    feeds(); sitemap()

if __name__ == "__main__":
    main()
