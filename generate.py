# Culture of Extensions — static SEO page generator
# Zero-JS pages, shared design tokens from the main site, full schema markup.
import json, html as H

DOMAIN = "https://www.cultureofextensions.com"
BOOK = "https://app.squareup.com/appointments/book/oireayuannjp07/LQYSJW8GJE1Y6/start"
PHONE = "(424) 428-9074"
PHONE_TEL = "+14244289074"
ADDR = "2119 N Glenoaks Blvd, Burbank, CA 91504"
EMAIL = "cultureofextensions@gmail.com"

SERVICES = [
    ("k-tip-extensions", "K-Tip Extensions", "From $700"),
    ("volume-density", "Volume & Density", "From $400"),
    ("length-transformation", "Length Transformation", "From $1,000"),
    ("bio-tape-color", "BIO Tape & Color", "From $500"),
]
CITIES = [
    ("hair-extensions-burbank", "Burbank"),
    ("hair-extensions-glendale", "Glendale"),
    ("hair-extensions-studio-city", "Studio City"),
    ("hair-extensions-toluca-lake", "Toluca Lake"),
    ("hair-extensions-pasadena", "Pasadena"),
    ("hair-extensions-los-angeles", "Los Angeles"),
]

def header():
    return f"""<header class="site"><div class="wrap">
<a class="logo" href="/">CULTURE <em>of</em> EXTENSIONS</a>
<nav class="main" aria-label="Primary">
<a href="/services/k-tip-extensions">K-Tip</a>
<a href="/services/length-transformation">Length</a>
<a href="/services/volume-density">Volume</a>
<a href="/hair-extensions-los-angeles">Service Areas</a>
<a href="{BOOK}" rel="noopener">Book</a>
</nav></div></header>"""

def footer():
    svc = "".join(f'<li><a href="/services/{s}">{n}</a></li>' for s, n, _ in SERVICES)
    cit = "".join(f'<li><a href="/{s}">Hair Extensions {c}</a></li>' for s, c in CITIES)
    return f"""<footer class="site"><div class="wrap"><div class="cols">
<div><p class="foot-label">Culture of Extensions · by Lana</p>
<p>{ADDR}<br><a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p style="margin-top:14px"><a class="btn ghost" style="padding:11px 24px;font-size:11px" href="{BOOK}" rel="noopener">Book Consultation</a></p></div>
<div><p class="foot-label">Signature Services</p><ul>{svc}</ul></div>
<div><p class="foot-label">Service Areas</p><ul>{cit}</ul></div>
</div></div></footer>"""

def page(path, title, desc, h1, eyebrow, lead, body, faq, img, img_alt, schema_extra):
    faq_html = "".join(
        f"<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>" for q, a in faq)
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    crumbs_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": f"{DOMAIN}/{path}"}]}
    schemas = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                      for s in [schema_extra, faq_schema, crumbs_schema] if s)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{DOMAIN}/{path}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{DOMAIN}/{path}">
<meta property="og:site_name" content="Culture of Extensions by Lana">
<meta name="geo.region" content="US-CA"><meta name="geo.placename" content="Burbank">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400..700;1,400..700&family=Inter:wght@200..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{schemas}
</head>
<body>
{header()}
<main>
<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> · {h1}</nav>
<div class="hero">
<div>
<p class="eyebrow">{eyebrow}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<a class="btn" href="{BOOK}" rel="noopener">Book Complimentary Consultation</a>
</div>
<img src="{img}" alt="{H.escape(img_alt)}" width="900" height="1200" fetchpriority="high" decoding="async" loading="lazy">
</div>
</div>
{body}
<div class="wrap">
<section aria-labelledby="faq">
<h2 id="faq">Questions, Answered</h2>
{faq_html}
</section>
<section class="cta" style="border-top:none">
<h2>Begin Your Transformation</h2>
<p>Complimentary, private consultation at our Burbank studio. Lana works with a select number of clients each month — consultations available in English, Spanish, and Russian.</p>
<a class="btn" href="{BOOK}" rel="noopener">Book Complimentary Consultation</a>
</section>
</div>
</main>
{footer()}
</body>
</html>"""

LB = {"@type":"HairSalon","name":"Culture of Extensions by Lana","@id":DOMAIN+"/#business",
      "telephone":PHONE_TEL,"address":{"@type":"PostalAddress","streetAddress":"2119 N Glenoaks Blvd",
      "addressLocality":"Burbank","addressRegion":"CA","postalCode":"91504","addressCountry":"US"}}

def svc_schema(name, price, path, desc):
    return {"@context":"https://schema.org","@type":"Service","name":name,
        "serviceType":"Hair extensions","url":f"{DOMAIN}/{path}","description":desc,
        "provider":LB,"areaServed":[{"@type":"City","name":c} for _,c in CITIES],
        "offers":{"@type":"Offer","priceCurrency":"USD","price":price.replace("From $","").replace(",","")}}

def city_schema(city, path, desc):
    return {"@context":"https://schema.org","@type":"Service","name":f"Hair Extensions in {city}, CA",
        "serviceType":"Hair extensions","url":f"{DOMAIN}/{path}","description":desc,
        "provider":LB,"areaServed":{"@type":"City","name":city}}

def cards(items):
    out = "".join(f'<div class="card"><span class="num">{i:02d}</span><h3>{t}</h3><p>{d}</p></div>'
                  for i,(t,d) in enumerate(items,1))
    return f'<div class="wrap"><section><div class="grid3">{out}</div></section></div>'

def block(h2_text, paras, checks=None):
    p = "".join(f'<p style="color:var(--dim);max-width:72ch;margin-bottom:16px">{x}</p>' for x in paras)
    c = ""
    if checks:
        c = '<ul class="checks">' + "".join(f"<li>{x}</li>" for x in checks) + "</ul>"
    return f'<div class="wrap"><section><h2>{h2_text}</h2>{p}{c}</section></div>'

import os
os.makedirs("services", exist_ok=True)
pages_written = []

# ============ SERVICE PAGES ============
svc_data = {
"k-tip-extensions": dict(
 title="K-Tip Hair Extensions in Burbank & Los Angeles | Culture of Extensions",
 desc="Signature K-Tip micro-capsule keratin extensions in Burbank, LA by Lana. Invisible bonds, zero-damage protocol, 100% Slavic & European hair. From $700.",
 h1="K-Tip Extensions, Architected for Invisibility",
 eyebrow="Signature Method · From $700",
 lead="Micro-capsule keratin bonds — our signature. Each capsule is shaped by hand around your natural strand for invisible integration, natural movement, and zero damage to your own hair.",
 img="/photos/g1.jpg", alt="K-Tip keratin bond hair extensions result on long hair, Burbank studio",
 body_cards=[("Micro-Capsule Precision","Capsules are formed smaller than industry standard and placed following your natural growth pattern — undetectable even in an updo."),("Zero-Damage Protocol","Attachment points are mapped to your hair density so no strand carries more weight than it can hold. Your natural hair stays healthy underneath."),("Slavic & European Hair","100% natural remy hair, color-matched to your roots, mid-lengths and ends — not just one flat tone.")],
 block_h2="Why K-Tip Is Our Signature",
 block_p=["K-Tip is the most precise extension method available: individual keratin capsules fused strand by strand, giving complete control over placement, density, and direction. It is the method Lana uses as her primary work because it allows for the highest level of invisible integration.","Every K-Tip appointment begins with a structural analysis of your natural hair. Method, strand count, capsule size, and placement map are decided before a single bond is fused. No templates — every installation is architected around you."],
 checks=["Invisible K-Tip integration — undetectable transition","Custom color blending across roots, lengths and ends","Personalized care guide and maintenance schedule included","Consultation and quote before any commitment"],
 faq=[("How long do K-Tip extensions last?","With proper care, K-Tip installations typically last 3–4 months before a move-up appointment. The hair itself can often be reused for multiple installations."),("Will K-Tip extensions damage my natural hair?","No — when installed correctly. Our zero-damage protocol maps every attachment point to your natural density so no strand is overloaded. Proper maintenance and timely move-up appointments protect your hair."),("How much do K-Tip extensions cost in Los Angeles?","At Culture of Extensions, K-Tip installations start from $700. The exact quote depends on strand count, length, and hair selected — you receive a personalized price at your complimentary consultation."),("Can K-Tip bonds be seen in thin or fine hair?","Our micro-capsules are smaller than standard and placed following your natural fall, so they remain invisible even in fine hair. Volume restoration is often a better option for very fine hair."),("How do I prepare for a K-Tip appointment?","Arrive with clean, dry hair, washed with clarifying shampoo and no conditioner or styling products. Everything else — analysis, color match, placement — is handled during your appointment.")]),
}

for slug, d in svc_data.items():
    name = [n for s,n,_ in SERVICES if s==slug][0]
    price = [p for s,_,p in SERVICES if s==slug][0]
    body = cards(d["body_cards"]) + block(d["block_h2"], d["block_p"], d["checks"])
    htm = page(f"services/{slug}", d["title"], d["desc"], d["h1"], d["eyebrow"], d["lead"],
               body, d["faq"], d["img"], d["alt"], svc_schema(name, price, f"services/{slug}", d["desc"]))
    open(f"services/{slug}.html","w").write(htm)
    pages_written.append(f"services/{slug}")
print("Service pages:", pages_written)
print("Generate.py updated: CSS external, lazy loading added")
