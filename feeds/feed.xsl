<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" doctype-system="about:legacy-compat"/>
<xsl:template match="/rss">
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title><xsl:value-of select="channel/title"/> · RSS feed</title>
<link rel="stylesheet" href="/assets/fonts/fonts.css"/>
<style>
:root{ --ink:#1B1840; --paper:#FBF8F1; --card:#FFFFFF; --muted:#6b6a76; --gold:#C9A227; }
*{ box-sizing:border-box; margin:0; }
body{ font-family:'Inter',system-ui,sans-serif; background:var(--paper); color:var(--ink); line-height:1.6; }
header{ background:var(--ink); color:#fff; padding:28px 24px; }
.wrap{ max-width:680px; margin:0 auto; padding:32px 24px 64px; }
header .mark{ font-family:'Space Grotesk','Inter',sans-serif; font-weight:700; font-size:1.25rem; letter-spacing:-.01em; }
header .mark span{ color:var(--gold); }
h1{ font-family:'Space Grotesk','Inter',sans-serif; font-size:1.75rem; margin:10px 0 6px; }
header p{ color:rgba(255,255,255,.78); font-size:.95rem; max-width:46ch; }
.hint{ background:var(--card); border:1px solid rgba(27,24,64,.12); border-radius:10px; padding:14px 18px; margin:0 0 28px; font-size:.95rem; }
.hint code{ font-family:ui-monospace,monospace; font-size:.85em; background:rgba(27,24,64,.06); padding:2px 6px; border-radius:4px; }
.item{ background:var(--card); border:1px solid rgba(27,24,64,.12); border-radius:10px; padding:18px 20px; margin-bottom:14px; }
.item h2{ font-family:'Source Serif 4',Georgia,serif; font-size:1.15rem; margin-bottom:4px; }
.item h2 a{ color:var(--ink); text-decoration:none; }
.item h2 a:hover{ text-decoration:underline; }
.item time{ color:var(--muted); font-size:.85rem; }
.item p{ color:var(--muted); font-size:.95rem; margin-top:6px; }
footer{ color:var(--muted); font-size:.85rem; }
footer a{ color:var(--ink); }
</style>
</head>
<body>
<header>
<div class="mark">kube<span>AI</span> publications</div>
<h1><xsl:value-of select="channel/title"/></h1>
<p><xsl:value-of select="channel/description"/></p>
</header>
<div class="wrap">
<div class="hint">This is the RSS feed for <a href="{channel/link}"><xsl:value-of select="channel/title"/></a>. To subscribe, copy the address of this page into your RSS reader, or read the magazine directly on the site.</div>
<xsl:for-each select="channel/item">
<div class="item">
<h2><a href="{link}"><xsl:value-of select="title"/></a></h2>
<time><xsl:value-of select="pubDate"/></time>
<p><xsl:value-of select="description"/></p>
</div>
</xsl:for-each>
<footer><p><a href="{channel/link}">Back to the magazine</a> · Published by kubeAI.</p></footer>
</div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
