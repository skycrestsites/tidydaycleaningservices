"""Static site builder for Tidy Day Cleaning Services.

Every page is written as <folder>/index.html so URLs never end in .html.
All internal links are relative, so the site works on any static host
(GitHub Pages project URL, custom domain, Netlify, Vercel, Cloudflare Pages).

Run from anywhere:  python _src/build.py
"""
import json, os, sys, datetime
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
VER = "3"

# ---------------------------------------------------------------- icons
ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "list": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "sparkle": '<path d="M12 3c.6 4.5 2.6 6.5 7 7-4.4.5-6.4 2.5-7 7-.6-4.5-2.6-6.5-7-7 4.4-.5 6.4-2.5 7-7Z"/><path d="M19 15c.2 1.6.9 2.3 2.5 2.5-1.6.2-2.3.9-2.5 2.5-.2-1.6-.9-2.3-2.5-2.5 1.6-.2 2.3-.9 2.5-2.5Z"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/>',
    "bed": '<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "hammer": '<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15 22 10.6"/><path d="m20.9 11.7-1.2-1.2c-.6-.6-1-1.4-1-2.3v-.8L16 4.6A5.6 5.6 0 0 0 12.1 3H9l.9.8A6.2 6.2 0 0 1 12 8.4V10l2 2h2.5l2.3 1.9"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
}


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


STAR = '<svg class="spark" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1c.9 6.6 4.4 10.1 11 11-6.6.9-10.1 4.4-11 11-.9-6.6-4.4-10.1-11-11 6.6-.9 10.1-4.4 11-11Z"/></svg>'


def e(s):
    return escape(s, quote=True)


# ---------------------------------------------------------------- shell
def head(p, title, desc, path, extra_ld=None, img="assets/og-image.jpg", preload=None):
    url = SITE + "/" + path
    ld = [business_ld()] + (extra_ld or [])
    pre = f'<link rel="preload" as="image" href="{p}assets/img/{preload}.webp" fetchpriority="high">\n' if preload else ""
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{e(NAME)}">
<meta name="theme-color" content="#FDF6F4">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Austin">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/{img}">
<link rel="icon" href="{p}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{p}assets/favicon-16.png">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..650;1,9..144,400..600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
{pre}<link rel="stylesheet" href="{p}css/styles.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": SITE + "/#business",
        "name": NAME,
        "description": "Home and small business cleaning in Austin, TX and surrounding areas: standard, deep, recurring, move-in and move-out, Airbnb, office and post-construction cleaning.",
        "url": SITE + "/",
        "logo": SITE + "/assets/logo.png",
        "image": SITE + "/assets/og-image.jpg",
        **({"email": EMAIL} if EMAIL else {}),
        **({"telephone": PHONE} if PHONE else {}),
        "founder": {"@type": "Person", "name": OWNER},
        "address": {"@type": "PostalAddress", "addressLocality": CITY, "addressRegion": REGION, "addressCountry": "US"},
        "areaServed": [{"@type": "City", "name": f"{a}, TX"} for a in AREAS],
        "priceRange": "$$",
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Cleaning Services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{SITE}/services/{s['slug']}/"}} for s in SERVICES],
        },
    }


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate(items)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def header(p, active=""):
    def cls(k):
        return ' aria-current="page"' if active == k else ""
    drop = "".join(f'<a href="{p}services/{s["slug"]}/">{icon(s["icon"])}<span>{e(s["nav"])}</span></a>' for s in SERVICES)
    mob = "".join(f'<a href="{p}services/{s["slug"]}/">{e(s["nav"])}</a>' for s in SERVICES)
    return f"""<div class="topbar"><div class="wrap topbar-in"><span>{icon("pin")} Serving {CITY}, {REGION} &amp; surrounding areas</span><a href="{p}contact/">Request a free quote {icon("arrow")}</a></div></div>
<header class="site-header" id="top">
  <div class="wrap nav">
    <a class="brand" href="{p}" aria-label="{e(NAME)} home"><img src="{p}assets/logo-sm.webp" alt="{e(NAME)}" width="440" height="225"></a>
    <nav class="menu" aria-label="Main">
      <a href="{p}"{cls("home")}>Home</a>
      <div class="has-drop">
        <a href="{p}services/" class="drop-trigger"{cls("services")} aria-haspopup="true">Services {icon("chev", "ic chev")}</a>
        <div class="drop"><div class="drop-in">{drop}<a class="drop-all" href="{p}services/">View all services {icon("arrow")}</a></div></div>
      </div>
      <a href="{p}about/"{cls("about")}>About</a>
      <a href="{p}#areas">Service Areas</a>
      <a href="{p}contact/"{cls("contact")}>Contact</a>
    </nav>
    <a class="btn btn-rose nav-cta" href="{p}contact/">Get a Free Quote</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav">{icon("menu")}</button>
  </div>
  <div class="mnav" id="mnav" hidden>
    <a href="{p}">Home</a>
    <p class="mnav-label">Services</p>
    <div class="mnav-sub">{mob}</div>
    <a href="{p}about/">About</a>
    <a href="{p}#areas">Service Areas</a>
    <a href="{p}contact/">Contact</a>
    <a class="btn btn-rose" href="{p}contact/">Get a Free Quote</a>
  </div>
</header>
<main id="main">
"""


def footer(p):
    svc = "".join(f'<li><a href="{p}services/{s["slug"]}/">{e(s["nav"])}</a></li>' for s in SERVICES)
    contact = ""
    if PHONE:
        contact += f'<li><a href="tel:{PHONE}">{icon("phone")} {e(PHONE)}</a></li>'
    if EMAIL:
        contact += f'<li><a href="mailto:{EMAIL}">{icon("mail")} {e(EMAIL)}</a></li>'
    contact += f'<li><span>{icon("pin")} {CITY}, {REGION} &amp; surrounding areas</span></li>'
    return f"""</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a href="{p}" class="foot-logo"><img src="{p}assets/logo-sm.webp" alt="{e(NAME)}" width="440" height="225" loading="lazy"></a>
      <p>Thoughtful, detail focused home and small business cleaning for {CITY} and the surrounding communities.</p>
    </div>
    <div><h3>Services</h3><ul>{svc}</ul></div>
    <div><h3>Company</h3><ul><li><a href="{p}about/">About Tidy Day</a></li><li><a href="{p}services/">All Services</a></li><li><a href="{p}#areas">Service Areas</a></li><li><a href="{p}#faq">FAQ</a></li><li><a href="{p}contact/">Contact</a></li></ul></div>
    <div><h3>Get in Touch</h3><ul class="foot-contact">{contact}</ul><a class="btn btn-rose btn-sm" href="{p}contact/">Request a Quote</a></div>
  </div>
  <div class="wrap foot-bottom"><p>&copy; <span data-year>{datetime.date.today().year}</span> {e(NAME)}. All rights reserved.</p><p>Proudly serving {CITY}, Texas</p></div>
</footer>
<a class="mobile-cta" href="{p}contact/">{icon("sparkle")} Get a Free Quote</a>
<script>window.TD_EMAIL={json.dumps(EMAIL)};</script>
<script src="{p}js/main.js?v={VER}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- blocks
def eyebrow(t):
    return f'<p class="eyebrow">{STAR}<span>{e(t)}</span></p>'


def img(p, name, alt, w, h, cls="", lazy=True, sizes=None):
    la = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img class="{cls}" src="{p}assets/img/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}"{la}>'


def service_cards(p, extra=True):
    cards = ""
    for s in SERVICES:
        cards += f"""<a class="svc-card" href="{p}services/{s['slug']}/">
  <div class="svc-img">{img(p, s['hero'], s['hero_alt'], 600, 420)}</div>
  <div class="svc-body"><span class="svc-ic">{icon(s['icon'])}</span><h3>{e(s['name'])}</h3><p>{e(s['short'])}</p><span class="more">Learn more {icon("arrow")}</span></div>
</a>"""
    if extra:
        cards += f"""<div class="svc-card svc-help"><div class="svc-body">
  <span class="svc-ic">{icon("heart")}</span><h3>Not sure what you need?</h3><p>Tell us a little about your space and we will recommend the right clean for your home and budget.</p>
  <a class="btn btn-ink btn-sm" href="{p}contact/">Talk to Us</a></div></div>"""
    return f'<div class="svc-grid">{cards}</div>'


def faq_block(faqs):
    items = "".join(f'<details class="faq"><summary><span>{e(q)}</span>{icon("chev", "ic chev")}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs)
    return f'<div class="faqs">{items}</div>'


def quote_form(p, preselect=""):
    opts = "".join(f'<option value="{e(s["name"])}" data-slug="{s["slug"]}"{" selected" if s["slug"] == preselect else ""}>{e(s["name"])}</option>' for s in SERVICES)
    return f"""<form class="quote-form" id="quote-form" novalidate>
  <div class="f-row">
    <label><span>Your name</span><input name="name" type="text" autocomplete="name" required placeholder="Jane Smith"></label>
    <label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(512) 000-0000"></label>
  </div>
  <div class="f-row">
    <label><span>Email</span><input name="email" type="email" autocomplete="email" required placeholder="you@email.com"></label>
    <label><span>City or ZIP</span><input name="city" type="text" autocomplete="postal-code" placeholder="Austin, 78704"></label>
  </div>
  <label><span>Service</span><select name="service" required><option value="">Choose a service</option>{opts}<option value="Not sure yet">Not sure yet</option></select></label>
  <label><span>Tell us about your space</span><textarea name="message" rows="4" placeholder="Bedrooms, bathrooms, pets, preferred day or anything we should know"></textarea></label>
  <button class="btn btn-rose btn-block" type="submit">Request My Free Quote {icon("arrow")}</button>
  <p class="form-note" role="status" aria-live="polite">We usually reply within one business day.</p>
</form>"""


def cta_band(p):
    return f"""<section class="cta-band">
  <div class="wrap cta-in">
    <div class="cta-copy">
      {eyebrow("Ready when you are")}
      <h2>Come home to a <em>tidy day.</em></h2>
      <p>Tell us about your space and we will put together a simple, personalized quote. No pressure and no long forms.</p>
      <div class="btns"><a class="btn btn-rose" href="{p}contact/">Get a Free Quote {icon("arrow")}</a><a class="btn btn-ghost" href="{p}services/">Explore Services</a></div>
    </div>
    <div class="cta-media">{img(p, "cta-supplies", "Pink gloved hand holding a yellow spray bottle against a mint background", 800, 533)}</div>
  </div>
</section>"""


def areas_block(p):
    chips = "".join(f'<li>{icon("pin")}{e(a)}</li>' for a in AREAS)
    return f"""<section class="section areas" id="areas">
  <div class="wrap areas-in">
    <div>
      {eyebrow("Service areas")}
      <h2>Cleaning homes across Austin &amp; Central Texas</h2>
      <p class="lede">From Central Austin bungalows to new builds in Leander and Kyle, we are proud to care for homes and businesses throughout the greater {CITY} area. Do not see your neighborhood? Reach out, we may still be able to help.</p>
      <a class="btn btn-ink" href="{p}contact/">Check Availability</a>
    </div>
    <ul class="chips">{chips}</ul>
  </div>
</section>"""


def page(path, html):
    out = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


# ---------------------------------------------------------------- pages
def home():
    p = ""
    ck = icon("check")
    inc = "".join('<div class="inc-col"><h3>' + e(k) + '</h3><ul class="ticks">' + "".join(f"<li>{ck}{e(x)}</li>" for x in v) + "</ul></div>" for k, v in INCLUDED.items())
    html = head(p, f"{NAME} | House Cleaning in Austin, TX",
                "Tidy Day Cleaning Services offers detail focused house cleaning in Austin, TX and surrounding areas. Standard, deep, recurring, move-out, Airbnb and office cleaning. Free quotes.",
                "", [faq_ld(HOME_FAQS)], preload="home-hero")
    html += header(p, "home")
    html += f"""<section class="hero">
  <div class="hero-deco" aria-hidden="true">{STAR}{STAR}{STAR}</div>
  <div class="wrap hero-in">
    <div class="hero-copy">
      {eyebrow("Home cleaning in Austin, TX")}
      <h1>A tidy home,<br>a <em>lighter</em> day.</h1>
      <p class="lede">Tidy Day Cleaning Services brings care, consistency and a little extra sparkle to homes across Austin and the surrounding areas, so you can spend your time on the things you love.</p>
      <div class="btns"><a class="btn btn-rose" href="{p}contact/">Get a Free Quote {icon("arrow")}</a><a class="btn btn-ghost" href="{p}services/">View Services</a></div>
      <ul class="hero-points"><li>{icon("check")}Owner led and detail focused</li><li>{icon("check")}Flexible scheduling</li><li>{icon("check")}Supplies included</li></ul>
    </div>
    <div class="hero-media">
      <div class="arch">{img(p, "home-hero", "Smiling cleaner vacuuming a bright, tidy living room", 1000, 1500, lazy=False)}</div>
      <div class="float-card"><span class="fc-ic">{icon("sparkle")}</span><div><strong>Every corner, every visit</strong><span>Checklist based cleaning</span></div></div>
    </div>
  </div>
</section>

<section class="trust">
  <div class="wrap trust-grid">
    <div>{icon("heart")}<div><strong>Personal care</strong><span>Your home treated like our own</span></div></div>
    <div>{icon("list")}<div><strong>Detailed checklists</strong><span>Nothing skipped, nothing rushed</span></div></div>
    <div>{icon("calendar")}<div><strong>Flexible scheduling</strong><span>One time or recurring visits</span></div></div>
    <div>{icon("pin")}<div><strong>Local to Austin</strong><span>Serving Central Texas</span></div></div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow("What we do")}
      <h2>Cleaning services for every kind of day</h2>
      <p class="lede">From weekly refreshes to move-out deep cleans, every service is built around a thorough checklist and a gentle, careful touch.</p>
    </div>
    {service_cards(p)}
  </div>
</section>

<section class="section tint-blush about-split" id="about">
  <div class="wrap split">
    <div class="split-media">
      <div class="frame frame-mint">{img(p, "about-kirsten", "Mint green cleaning gloves and a spray bottle resting beside a potted plant", 800, 1067)}</div>
    </div>
    <div class="split-copy">
      {eyebrow("Meet Tidy Day")}
      <h2>Cleaning with a <em>personal</em> touch</h2>
      <p>Tidy Day Cleaning Services was founded by {OWNER} with a simple idea: a clean home should feel calm, cared for and completely yours. We are a local Austin company that believes the little details are what make a clean feel truly finished.</p>
      <p>Every visit follows a thoughtful checklist, and every client gets the kind of friendly, respectful service we would want in our own homes. Whether you need a one time reset or a regular helping hand, we are here to make your days a little lighter.</p>
      <ul class="ticks two">
        <li>{icon("check")}Owner led and locally run</li><li>{icon("check")}Clear, friendly communication</li>
        <li>{icon("check")}Respect for your home and pets</li><li>{icon("check")}Consistent, detail focused results</li>
      </ul>
      <a class="text-link" href="{p}about/">More about us {icon("arrow")}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow("How it works")}
      <h2>Three simple steps to a cleaner home</h2>
    </div>
    <ol class="steps">
      <li><span class="step-n">01</span><h3>Request a quote</h3><p>Share a few details about your home, the service you need and your ideal timing.</p></li>
      <li><span class="step-n">02</span><h3>We plan your clean</h3><p>We confirm your quote, talk through priorities and schedule a time that works for you.</p></li>
      <li><span class="step-n">03</span><h3>Enjoy your tidy day</h3><p>Our team arrives prepared and leaves your space fresh, organized and spotless.</p></li>
    </ol>
  </div>
</section>

<section class="section tint-sky">
  <div class="wrap included">
    <div class="inc-head">
      {eyebrow("What is included")}
      <h2>A thorough clean, room by room</h2>
      <p class="lede">Here is a look at what every standard visit covers. Deep cleans and move-out cleans go even further.</p>
      <div class="inc-img">{img(p, "included-kitchen", "Bright, freshly cleaned kitchen with granite island and stainless appliances", 1080, 720)}</div>
    </div>
    <div class="inc-cols">{inc}
      <div class="inc-col inc-add"><h3>Popular add ons</h3><p>Inside oven, inside refrigerator, interior windows, inside cabinets, laundry and dishes.</p></div>
    </div>
  </div>
</section>

{areas_block(p)}

<section class="section tint-mint" id="faq">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      {eyebrow("Questions")}
      <h2>Frequently asked questions</h2>
      <p class="lede">Have a question that is not answered here? We are always happy to help.</p>
      <a class="btn btn-ink" href="{p}contact/">Ask Us Anything</a>
    </div>
    {faq_block(HOME_FAQS)}
  </div>
</section>

{cta_band(p)}
"""
    html += footer(p)
    page("", html)


def services_index():
    p = "../"
    html = head(p, f"Cleaning Services in Austin, TX | {NAME}",
                "Explore house cleaning services in Austin, TX from Tidy Day: standard, deep, recurring, move-in and move-out, Airbnb, office and post-construction cleaning.",
                "services/", [crumbs_ld([("Home", ""), ("Services", "services/")])], img="assets/og-image.jpg")
    html += header(p, "services")
    html += f"""<section class="page-hero">
  <div class="wrap page-hero-in">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}">Home</a><span>/</span><span aria-current="page">Services</span></nav>
    {eyebrow("Our services")}
    <h1>Cleaning services for <em>Austin</em> homes &amp; businesses</h1>
    <p class="lede">Whatever your space needs, we have a thoughtful, detail focused clean for it. Choose a service below to see exactly what is included.</p>
  </div>
</section>
<section class="section pt-0">
  <div class="wrap">{service_cards(p)}</div>
</section>
{areas_block(p)}
{cta_band(p)}
"""
    html += footer(p)
    page("services", html)


def service(s):
    p = "../../"
    path = f"services/{s['slug']}/"
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    inc = "".join(f"<li>{icon('check')}{e(x)}</li>" for x in s["includes"])
    ideal = "".join(f"<li>{icon('heart')}{e(x)}</li>" for x in s["ideal"])
    body = "".join(f"<p>{e(x)}</p>" for x in s["body"])
    (g1, a1), (g2, a2) = s["gallery"]
    other = "".join(f'<a href="{p}services/{o["slug"]}/">{icon(o["icon"])}<span>{e(o["name"])}</span>{icon("arrow", "ic go")}</a>' for o in others)
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
              "description": s["meta"], "url": SITE + "/" + path, "provider": {"@id": SITE + "/#business"},
              "areaServed": [{"@type": "City", "name": f"{a}, TX"} for a in AREAS],
              "image": f"{SITE}/assets/img/{s['hero']}.webp"}
    html = head(p, f"{s['title']} | {SHORT}", s["meta"], path,
                [svc_ld, crumbs_ld([("Home", ""), ("Services", "services/"), (s["name"], path)]), faq_ld(s["faqs"])],
                preload=s["hero"])
    html += header(p, "services")
    html += f"""<section class="svc-hero">
  <div class="wrap svc-hero-in">
    <div class="svc-hero-copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}">Home</a><span>/</span><a href="{p}services/">Services</a><span>/</span><span aria-current="page">{e(s['nav'])}</span></nav>
      {eyebrow(s['name'])}
      <h1>{e(s['title'].replace(' in Austin, TX', ''))} <em>in Austin, TX</em></h1>
      <p class="lede">{e(s['lead'])}</p>
      <div class="btns"><a class="btn btn-rose" href="{p}contact/?service={s['slug']}">Get a Free Quote {icon("arrow")}</a><a class="btn btn-ghost" href="#included">What is included</a></div>
    </div>
    <div class="svc-hero-media">{img(p, s['hero'], s['hero_alt'], 1600, 1067, "", lazy=False)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split split-top">
    <div class="split-copy">
      {eyebrow("Overview")}
      <h2>Why Austin clients choose our {e(s['name'].lower())}</h2>
      {body}
      <div class="ideal"><h3>Ideal for</h3><ul>{ideal}</ul></div>
    </div>
    <div class="duo">
      <figure>{img(p, g1, a1, 1100, 733)}</figure>
      <figure>{img(p, g2, a2, 1100, 733)}</figure>
    </div>
  </div>
</section>

<section class="section tint-blush" id="included">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow("Checklist")}
      <h2>What is included</h2>
      <p class="lede">Every {e(s['name'].lower())} follows this checklist. Have something specific in mind? Just let us know when you request your quote.</p>
    </div>
    <ul class="checklist">{inc}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow("Our process")}
      <h2>Simple from start to sparkle</h2>
    </div>
    <ol class="steps">
      <li><span class="step-n">01</span><h3>Tell us about your space</h3><p>Send a quick request with your home size, service and timing.</p></li>
      <li><span class="step-n">02</span><h3>Get a clear quote</h3><p>We confirm the details, answer questions and lock in a time.</p></li>
      <li><span class="step-n">03</span><h3>Relax, it is handled</h3><p>We arrive prepared and leave everything fresh and spotless.</p></li>
    </ol>
  </div>
</section>

<section class="section tint-mint">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      {eyebrow("Questions")}
      <h2>{e(s['name'])} FAQ</h2>
      <p class="lede">Do not see your question? Send us a message and we will get right back to you.</p>
    </div>
    {faq_block(s['faqs'])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow("Explore more")}
      <h2>Other services</h2>
    </div>
    <div class="other-svc">{other}</div>
  </div>
</section>

{cta_band(p)}
"""
    html += footer(p)
    page(path.rstrip("/"), html)


def about():
    p = "../"
    html = head(p, f"About Us | {NAME} in Austin, TX",
                f"Meet Tidy Day Cleaning Services, a locally owned Austin, TX cleaning company founded by {OWNER}. Detail focused, friendly and dependable.",
                "about/", [crumbs_ld([("Home", ""), ("About", "about/")])])
    html += header(p, "about")
    html += f"""<section class="page-hero">
  <div class="wrap page-hero-in">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}">Home</a><span>/</span><span aria-current="page">About</span></nav>
    {eyebrow("About us")}
    <h1>Bringing calm, clean <em>days</em> to Austin homes</h1>
    <p class="lede">We are a locally owned cleaning company built on care, consistency and the belief that a clean home can change the whole feel of your day.</p>
  </div>
</section>
<section class="section pt-0">
  <div class="wrap split">
    <div class="split-media"><div class="frame frame-sky">{img(p, "about-kirsten", "Mint green cleaning gloves and a spray bottle resting beside a potted plant", 800, 1067)}</div></div>
    <div class="split-copy">
      {eyebrow("Our story")}
      <h2>Founded by {e(OWNER)}</h2>
      <p>Tidy Day Cleaning Services started with a simple goal: give busy Austin families and professionals a cleaning service they can genuinely count on. Not a rushed wipe down, but a careful, thorough clean that leaves your home feeling light and refreshed.</p>
      <p>We know that inviting someone into your home is personal. That is why we focus on clear communication, showing up when we say we will and treating every room, pet and personal item with respect.</p>
      <p>Today we care for homes, rentals and small businesses across Austin and the surrounding communities, and we would love to care for yours too.</p>
    </div>
  </div>
</section>
<section class="section tint-sky">
  <div class="wrap">
    <div class="sec-head center">{eyebrow("What we value")}<h2>The Tidy Day difference</h2></div>
    <div class="values">
      <div>{icon("heart")}<h3>Care in every detail</h3><p>We clean the way we would want our own homes cleaned, with patience and pride.</p></div>
      <div>{icon("list")}<h3>Consistent checklists</h3><p>Every visit follows a proven checklist so your results are reliable every time.</p></div>
      <div>{icon("smile")}<h3>Friendly communication</h3><p>Questions, changes or special requests are always easy and welcome.</p></div>
      <div>{icon("key")}<h3>Respect for your home</h3><p>Your space, your belongings and your pets are always treated with care.</p></div>
    </div>
  </div>
</section>
{areas_block(p)}
{cta_band(p)}
"""
    html += footer(p)
    page("about", html)


def contact():
    p = "../"
    html = head(p, f"Contact Us & Free Quote | {NAME}",
                "Request a free house cleaning quote from Tidy Day Cleaning Services in Austin, TX. Standard, deep, recurring, move-out, Airbnb, office and post-construction cleaning.",
                "contact/", [crumbs_ld([("Home", ""), ("Contact", "contact/")])])
    html += header(p, "contact")
    rows = ""
    if PHONE:
        rows += f'<li>{icon("phone")}<div><strong>Call or text</strong><a href="tel:{PHONE}">{e(PHONE)}</a></div></li>'
    if EMAIL:
        rows += f'<li>{icon("mail")}<div><strong>Email</strong><a href="mailto:{EMAIL}">{e(EMAIL)}</a></div></li>'
    rows += f'<li>{icon("pin")}<div><strong>Service area</strong><span>{CITY}, {REGION} &amp; surrounding areas</span></div></li>'
    rows += f'<li>{icon("clock")}<div><strong>Response time</strong><span>Usually within one business day</span></div></li>'
    html += f"""<section class="page-hero">
  <div class="wrap page-hero-in">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}">Home</a><span>/</span><span aria-current="page">Contact</span></nav>
    {eyebrow("Free quote")}
    <h1>Let us make your next day a <em>tidy</em> one</h1>
    <p class="lede">Tell us a little about your space and the service you need. We will follow up with a personalized quote, usually within one business day.</p>
  </div>
</section>
<section class="section pt-0" id="quote">
  <div class="wrap contact-grid">
    <div class="form-card">
      <h2>Request your free quote</h2>
      {quote_form(p)}
    </div>
    <aside class="contact-side">
      <ul class="contact-list">{rows}</ul>
      <div class="side-img">{img(p, "standard-spray", "Spraying and wiping a kitchen surface with a striped cloth", 1100, 825)}</div>
      <div class="side-note">{icon("sparkle")}<p>First time with us? Ask about starting with a deep clean, then keeping things fresh with recurring visits.</p></div>
    </aside>
  </div>
</section>
{areas_block(p)}
"""
    html += footer(p)
    page("contact", html)


def not_found():
    # 404 lives at the root but may be served from any depth, so use absolute root links on the custom domain
    p = "/"
    html = head(p, f"Page Not Found | {NAME}", "The page you are looking for could not be found.", "404")
    html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    html += header(p)
    html += f"""<section class="page-hero nf">
  <div class="wrap page-hero-in center">
    {eyebrow("Error 404")}
    <h1>Oops, this page <em>swept</em> away.</h1>
    <p class="lede">The page you are looking for has moved or no longer exists. Let us help you find your way.</p>
    <div class="btns center"><a class="btn btn-rose" href="/">Back to Home</a><a class="btn btn-ghost" href="/services/">View Services</a></div>
  </div>
</section>
"""
    html += footer(p)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def extras():
    urls = [("", "1.0"), ("services/", "0.9"), ("about/", "0.7"), ("contact/", "0.8")] + [(f"services/{s['slug']}/", "0.8") for s in SERVICES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, pr in urls:
        sm += f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
    sm += "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    man = {"name": NAME, "short_name": SHORT, "start_url": "./", "display": "standalone", "background_color": "#FDF6F4", "theme_color": "#FDF6F4",
           "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8", newline="\n").write(json.dumps(man, indent=2))


if __name__ == "__main__":
    home(); services_index(); about(); contact(); not_found(); extras()
    for s in SERVICES:
        service(s)
    print("Built", 5 + len(SERVICES), "pages")
