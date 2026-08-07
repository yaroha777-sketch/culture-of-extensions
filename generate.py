# Culture of Extensions — static SEO page generator
# Zero-JS pages, shared design tokens from the main site, full schema markup.
import json, html as H

DOMAIN = "https://www.cultureofextensions.com"
BOOK = "https://app.squareup.com/appointments/book/oireayuannjp07/LQYSJW8GJE1Y6/start"
PHONE = "(424) 428-9074"
PHONE_TEL = "+14244289074"
ADDR = "2119 N Glenoaks Blvd, Burbank, CA 91504"
EMAIL = "cultureofextensions@gmail.com"
INSTAGRAM = "https://www.instagram.com/culture_of_extensions/"
GOOGLE_ADS_ID = "AW-6297879762"

CSS = """
:root{--bg:#131210;--ink:#EDE8DC;--gold:#C9B896;--dim:#9d978a;--line:rgba(201,184,150,.18)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font:300 17px/1.7 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.serif{font-family:"Bodoni Moda",serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
header.site{position:sticky;top:0;z-index:50;background:rgba(19,18,16,.85);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;justify-content:space-between;align-items:center;height:64px}
.logo{font-family:"Bodoni Moda",serif;font-size:19px;letter-spacing:.06em;color:var(--ink);text-decoration:none}
.logo em{color:var(--gold);font-style:italic}
nav.main{display:flex;gap:28px}
nav.main a{color:var(--dim);text-decoration:none;font-size:12px;letter-spacing:.18em;text-transform:uppercase;transition:color .2s}
nav.main a:hover,nav.main a:focus{color:var(--gold)}
.btn{display:inline-block;background:var(--gold);color:#131210;padding:15px 34px;text-decoration:none;font-weight:400;font-size:13px;letter-spacing:.16em;text-transform:uppercase;transition:opacity .2s}
.btn:hover{opacity:.85}
.btn.ghost{background:none;border:1px solid var(--gold);color:var(--gold)}
.crumbs{padding:22px 0 0;font-size:12px;letter-spacing:.1em;color:var(--dim)}
.crumbs a{color:var(--dim);text-decoration:none}
.crumbs a:hover{color:var(--gold)}
.hero{padding:56px 0 64px;display:grid;grid-template-columns:1.2fr .8fr;gap:56px;align-items:center}
.hero .eyebrow{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--gold);margin-bottom:18px}
h1{font-family:"Bodoni Moda",serif;font-weight:500;font-size:clamp(34px,5vw,58px);line-height:1.08;letter-spacing:.01em;background:linear-gradient(135deg,#EDE8DC 30%,#C9B896 75%,#a8946c);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:22px}
.hero p.lead{color:var(--dim);max-width:54ch;margin-bottom:32px}
.hero img{width:100%;height:auto;display:block;border:1px solid var(--line)}
h2{font-family:"Bodoni Moda",serif;font-weight:500;font-size:clamp(26px,3.4vw,38px);color:var(--ink);margin:0 0 18px}
h3{font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:400;margin-bottom:10px}
section{padding:56px 0;border-top:1px solid var(--line)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.card{border:1px solid var(--line);padding:30px}
.card p{color:var(--dim);font-size:15.5px}
.num{font-family:"Bodoni Moda",serif;color:var(--gold);font-size:30px;display:block;margin-bottom:12px}
ul.checks{list-style:none;color:var(--dim)}
ul.checks li{padding:10px 0 10px 30px;position:relative;border-bottom:1px solid var(--line)}
ul.checks li::before{content:"✦";position:absolute;left:2px;color:var(--gold);font-size:12px}
details{border-bottom:1px solid var(--line)}
details summary{cursor:pointer;padding:20px 0;font-size:17px;color:var(--ink);list-style:none;display:flex;justify-content:space-between;align-items:center}
details summary::after{content:"+";color:var(--gold);font-size:22px;font-family:"Bodoni Moda",serif}
details[open] summary::after{content:"–"}
details p{color:var(--dim);padding:0 0 22px;max-width:70ch}
.cta{padding:72px 0;text-align:center}
.cta p{color:var(--dim);max-width:56ch;margin:0 auto 30px}
footer.site{border-top:1px solid var(--line);padding:48px 0;font-size:14px;color:var(--dim)}
footer.site .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:36px}
footer.site a{color:var(--dim);text-decoration:none}
footer.site a:hover{color:var(--gold)}
footer.site ul{list-style:none}
footer.site li{padding:4px 0}
.foot-label{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin-bottom:12px}
@media(max-width:840px){.hero{grid-template-columns:1fr;padding:40px 0}.grid2,.grid3,footer.site .cols{grid-template-columns:1fr}nav.main{display:none}section{padding:44px 0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

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



def tracking_head():
    return """<!-- Google tag (Google Ads) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={google_ads_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() {{ window.dataLayer.push(arguments); }}
  window.gtag = window.gtag || gtag;
  window.gtag("js", new Date());
  window.gtag("config", "{google_ads_id}", {{
    send_page_view: true,
    business_vertical: "premium_hair_extensions",
    market: "Los Angeles",
    local_market: "Burbank / Glendale / Los Angeles"
  }});

  window.coeTrack = function(eventName, properties) {{
    var payload = Object.assign({{
      event: eventName,
      page_path: window.location.pathname,
      page_location: window.location.href,
      page_title: document.title,
      market: "Los Angeles",
      local_market: "Burbank / Glendale / Los Angeles",
      business_vertical: "premium_hair_extensions"
    }}, properties || {{}});

    window.dataLayer.push(payload);

    if (typeof window.gtag === "function") {{
      window.gtag("event", eventName, payload);
    }}
  }};
  window.coeTrack("coe_page_view", {{ engagement_type: "page_view" }});
</script>""".format(google_ads_id=GOOGLE_ADS_ID)


def tracking_body():
    return r"""<script>
  (function() {
    function normalizeText(value) {
      return (value || "").replace(/\s+/g, " ").trim().slice(0, 120);
    }

    function normalizeUrl(href) {
      try {
        return new URL(href, window.location.href);
      } catch (error) {
        return null;
      }
    }

    function sectionIdFor(link) {
      var section = link.closest && link.closest("section");
      return section ? section.id || undefined : undefined;
    }

    function trackClick(eventName, link, extra) {
      var href = link.getAttribute("href") || "";
      var url = normalizeUrl(href);
      var payload = Object.assign({
        link_url: href,
        link_domain: url ? url.hostname : undefined,
        link_text: normalizeText(link.innerText || link.getAttribute("aria-label") || link.title),
        section_id: sectionIdFor(link),
        click_source: "site_cta"
      }, extra || {});

      window.coeTrack(eventName, payload);
    }

    document.addEventListener("click", function(event) {
      var link = event.target.closest && event.target.closest("a");
      if (!link || typeof window.coeTrack !== "function") return;

      var href = link.getAttribute("href") || "";
      var hrefLower = href.toLowerCase();

      if (hrefLower.indexOf("app.squareup.com/appointments") !== -1 || hrefLower.indexOf("squareup.com/appointments") !== -1) {
        trackClick("coe_booking_click", link, {
          conversion_type: "booking_intent",
          lead_channel: "square_booking",
          lead_priority: "primary",
          value: 1,
          currency: "USD"
        });
        return;
      }

      if (hrefLower.indexOf("instagram.com") !== -1) {
        trackClick("coe_instagram_click", link, {
          conversion_type: "social_intent",
          lead_channel: "instagram",
          social_platform: "instagram",
          lead_priority: "secondary"
        });
        return;
      }

      if (hrefLower.indexOf("tel:") === 0) {
        trackClick("coe_phone_click", link, {
          conversion_type: "phone_lead",
          lead_channel: "phone",
          lead_priority: "secondary"
        });
        return;
      }

      if (hrefLower.indexOf("mailto:") === 0) {
        trackClick("coe_email_click", link, {
          conversion_type: "email_lead",
          lead_channel: "email",
          lead_priority: "secondary"
        });
        return;
      }

      if (href.charAt(0) === "#") {
        trackClick("coe_navigation_click", link, {
          conversion_type: "site_engagement",
          destination_section: href
        });
        return;
      }

      var url = normalizeUrl(href);
      if (url && url.hostname !== window.location.hostname) {
        trackClick("coe_external_click", link, {
          conversion_type: "external_engagement",
          lead_priority: "diagnostic"
        });
      }
    }, true);
  })();
</script>"""

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
<p>{ADDR}<br><a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{INSTAGRAM}" rel="noopener">Instagram @culture_of_extensions</a></p>
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
<style>{CSS}</style>
{tracking_head()}
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
<img src="{img}" alt="{H.escape(img_alt)}" width="900" height="1200" fetchpriority="high" decoding="async">
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
{tracking_body()}
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
 body_cards=[("Micro-Capsule Precision","Capsules are formed smaller than industry standard and placed following your natural growth pattern — undetectable even in an updo."),
  ("Zero-Damage Protocol","Attachment points are mapped to your hair density so no strand carries more weight than it can hold. Your natural hair stays healthy underneath."),
  ("Slavic & European Hair","100% natural remy hair, color-matched to your roots, mid-lengths and ends — not just one flat tone.")],
 block_h2="Why K-Tip Is Our Signature",
 block_p=["K-Tip is the most precise extension method available: individual keratin capsules fused strand by strand, giving complete control over placement, density, and direction. It is the method Lana has refined across 14+ years and 2,500+ transformations — and the foundation of the Culture of Extensions methodology.",
 "Every K-Tip appointment begins with a structural analysis of your natural hair. Method, strand count, capsule size, and placement map are decided before a single bond is fused. No templates — your hair is architected individually."],
 checks=["Invisible K-Tip integration — undetectable transition","Custom color blending across roots, lengths and ends","Personalized care guide and maintenance schedule included","Consultations in English, Spanish, and Russian"],
 faq=[("How long do K-Tip extensions last?","With proper care, K-Tip installations typically last 3–4 months before a move-up appointment. The hair itself can often be reused for multiple installations — your personalized maintenance schedule is included."),
  ("Will K-Tip extensions damage my natural hair?","No — when installed correctly. Our zero-damage protocol maps every attachment point to your natural density so no strand is overloaded. Protecting your natural hair is the first principle of every plan."),
  ("How much do K-Tip extensions cost in Los Angeles?","At Culture of Extensions, K-Tip installations start from $700. The exact quote depends on strand count, length, and hair selected — you receive a personalized plan and exact price at your complimentary consultation."),
  ("Can K-Tip bonds be seen in thin or fine hair?","Our micro-capsules are smaller than standard and placed following your natural fall, so they remain invisible even in fine hair. Volume restoration in fine hair is one of our most requested transformations."),
  ("How do I prepare for a K-Tip appointment?","Arrive with clean, dry hair, washed with clarifying shampoo and no conditioner or styling products. Everything else — analysis, color match, placement map — happens at the consultation.")]),
"volume-density": dict(
 title="Volume & Density Hair Extensions in Burbank, LA | Culture of Extensions",
 desc="Targeted volume and density restoration for fine hair in Burbank & Los Angeles. Micro-capsule placement by Lana — natural fullness, zero damage. From $400.",
 h1="Volume & Density, Restored Naturally",
 eyebrow="Targeted Placement · From $400",
 lead="Targeted micro-capsule placement to restore fullness and natural abundance — designed for fine hair that needs body, not just length.",
 img="/photos/g3.jpg", alt="Natural volume restoration with hair extensions on fine hair, Los Angeles",
 body_cards=[("Built for Fine Hair","Lightweight micro-capsules sized for fine strands — fullness without strain on your natural hair."),
  ("Strategic Mapping","Volume is placed where your hair actually needs it: crown, sides, or perimeter — not a uniform template."),
  ("Invisible in Any Style","Placement follows your parting and styling habits so density looks born, not added.")],
 block_h2="Density Without Compromise",
 block_p=["Fine hair carries extensions differently — which is why volume work demands more precision than any other installation. Lana's approach starts with an honest structural analysis: where your hair can hold weight, where it cannot, and how much density it can carry while staying healthy.",
 "The result is fullness that moves naturally, photographs beautifully, and protects the hair you grow yourself. This is the difference between adding hair and architecting density."],
 checks=["Featherweight micro-capsules for fine hair","Placement mapped to your parting and lifestyle","Natural hair health monitored at every appointment","From $400 — exact plan at complimentary consultation"],
 faq=[("Is my hair too thin for extensions?","In most cases, no — it needs the right method, not more hair. Micro-capsule volume work is specifically designed for fine hair. The consultation includes an honest assessment; if extensions would compromise your hair, Lana will tell you."),
  ("How is volume placement different from length extensions?","Volume placement targets specific zones — crown, sides, perimeter — with fewer, lighter strands. Length transformation extends your entire perimeter. Many clients combine both in one plan."),
  ("What does volume restoration cost?","Volume and density work starts from $400. Your exact quote depends on the zones treated and strand count — defined in your personalized plan at the complimentary consultation."),
  ("Will anyone be able to tell I have extensions?","No. Our philosophy is invisible artistry: texture, porosity, and movement are matched so precisely that even hairdressers can't see the transition."),
  ("How often does volume work need maintenance?","Move-up appointments typically fall every 8–12 weeks depending on your growth rate. You leave with a personalized maintenance schedule and direct access to Lana for questions.")]),
"length-transformation": dict(
 title="Length Transformation Extensions in Burbank & LA | Culture of Extensions",
 desc="Full-length bespoke hair extensions in 100% Slavic & European remy hair. Burbank studio serving Los Angeles. By Lana — from $1,000.",
 h1="Length Transformation in Slavic & European Hair",
 eyebrow="Full Bespoke Installation · From $1,000",
 lead="Full-length bespoke extensions in 100% Slavic and European remy hair — the most coveted hair in the world, architected around your natural foundation.",
 img="/photos/g5.jpg", alt="Full length transformation with Slavic hair extensions, Burbank Los Angeles",
 body_cards=[("100% Slavic & European Remy","The finest natural hair available — fine cuticle, natural shine, and movement that blends seamlessly with your own."),
  ("Length Architecture","Length is designed in proportion to your features, density, and lifestyle — not pulled from a chart."),
  ("A Ritual, Not a Service","Meticulous, unhurried placement. Every bond positioned so the result is invisible and weightless.")],
 block_h2="The Difference Slavic Hair Makes",
 block_p=["Slavic and European hair is naturally fine, soft, and light — the closest match to most natural textures and the only hair we install. It accepts toning without aggressive processing, holds its quality across months of wear, and moves like your own hair because structurally it is the same.",
 "A full length transformation at Culture of Extensions is a complete design process: strand count, color blending across three zones, length mapping, and a finishing cut that integrates the new length into your natural shape."],
 checks=["100% Slavic & European remy hair only — no compromises","Three-zone color matching: roots, mid-lengths, ends","Finishing cut and styling included in installation","Personalized care guide and direct access to Lana"],
 faq=[("Why is Slavic hair considered the best for extensions?","Slavic hair is naturally fine and soft with an intact cuticle, so it blends with most natural textures, takes toning gently, and keeps its shine for months. It is the only hair we install."),
  ("How long can I go?","Length is architected in proportion to your natural density and lifestyle. At your consultation Lana maps what your hair can carry healthily — most clients achieve dramatic length while keeping natural movement."),
  ("What does a full length transformation cost?","Full-length bespoke installations start from $1,000, depending on length, strand count, and hair weight. You receive an exact personalized quote at your complimentary consultation."),
  ("How long does the installation take?","A full transformation is an unhurried, meticulous process — typically several hours including the finishing cut. Exact timing is confirmed with your personalized plan."),
  ("Can I color or tone the extensions later?","Slavic hair accepts transparent keratin toning beautifully — no dye, no damage. Color adjustments are planned with Lana so the hair keeps its integrity across its full lifespan.")]),
"bio-tape-color": dict(
 title="BIO Tape Extensions & Keratin Toning in Burbank, LA | Culture of Extensions",
 desc="Ultra-thin seamless BIO tape wefts and transparent keratin toning in Burbank, Los Angeles. No dye, no damage — by Lana. From $500.",
 h1="BIO Tape & Transparent Keratin Color",
 eyebrow="Seamless Wefts · From $500",
 lead="Ultra-thin seamless wefts and transparent keratin toning — color refinement and density with no dye and no damage.",
 img="/photos/g7.jpg", alt="Seamless BIO tape weft extensions with keratin toning, Burbank salon",
 body_cards=[("Ultra-Thin Wefts","BIO tape sits flat against the scalp — invisible at the parting, comfortable from day one."),
  ("Keratin Toning","Transparent toning refines color without oxidative dye — shine and tone, zero chemical damage."),
  ("Fast, Gentle, Reversible","Shorter installation time and gentle removal make BIO tape ideal for first-time extension clients.")],
 block_h2="Color Without Chemistry",
 block_p=["Transparent keratin toning is how we adjust tone across your installation — warming, cooling, or glossing the hair — without a single drop of oxidative dye. The hair keeps its structure; you keep the color precision.",
 "Paired with ultra-thin BIO tape wefts, this is our gentlest installation: seamless density and refined color in a single appointment, with the same zero-damage standard as every Culture of Extensions method."],
 checks=["Seamless wefts invisible at the parting","Transparent keratin gloss — no oxidative dye","Ideal entry method for first-time clients","From $500 — exact plan at consultation"],
 faq=[("What is BIO tape and how is it different from regular tape-ins?","BIO tape wefts are ultra-thin and flexible, sitting flush against the scalp. They are lighter and less detectable than standard tape-ins and remove gently without residue."),
  ("What is transparent keratin toning?","A no-dye color refinement: transparent keratin pigment glosses the hair, adjusting tone and adding shine without oxidative chemistry. It keeps both your natural hair and the extension hair structurally intact."),
  ("How long does BIO tape last?","Tape installations are typically maintained every 6–8 weeks, when wefts are lifted and re-applied. The hair itself is reusable across multiple cycles with proper care."),
  ("Is BIO tape good for first-time extension wearers?","Yes — it is our most gentle and reversible method, with a shorter installation time. Many clients start with BIO tape and move to K-Tip as they commit to longer wear."),
  ("Can I combine BIO tape with K-Tip?","Yes. Hybrid plans are common: tape wefts for overall density with K-Tip strands framing the face and parting. Your combination is designed at the complimentary consultation.")]),
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

# ============ CITY PAGES ============
city_data = {
"hair-extensions-burbank": dict(city="Burbank",
 title="Hair Extensions in Burbank, CA | K-Tip & BIO Tape by Lana",
 desc="Premium hair extension studio in Burbank, CA. K-Tip micro-capsule & BIO tape in 100% Slavic hair by Lana — 14+ years, 2,500+ transformations. Book a free consultation.",
 h1="Hair Extensions in Burbank, California",
 eyebrow="Our Studio · Home Base",
 lead="Culture of Extensions is based on N Glenoaks Blvd in Burbank — a private, appointment-only studio where every transformation is architected individually by Lana.",
 img="/photos/g2.jpg", alt="Premium hair extensions result at Burbank studio, Culture of Extensions",
 local=["Our studio at 2119 N Glenoaks Blvd is the home of the Culture of Extensions methodology: K-Tip micro-capsule and BIO tape installations in 100% Slavic and European remy hair, architected around your natural hair, density, and color.",
 "Burbank clients visit us from Magnolia Park, the Rancho district, the Media District, and the hillside neighborhoods — most within a 10-minute drive. Street parking is available near the studio, and every appointment is private: one client, full attention."],
 checks=["Private appointment-only studio on N Glenoaks Blvd","Complimentary consultation before any commitment","Consultations in English, Spanish, and Russian","Direct access to Lana between appointments"],
 faq=[("Where exactly is the studio located in Burbank?","2119 N Glenoaks Blvd, Burbank, CA 91504 — in the northern part of Burbank, minutes from the 5 freeway. Visits are by appointment only; book a complimentary consultation to begin."),
  ("How much do hair extensions cost in Burbank?","Installations at our Burbank studio start from $400 for volume work, $500 for BIO tape, $700 for signature K-Tip, and $1,000 for full length transformations. Exact pricing follows your personalized plan."),
  ("Do I need a consultation before booking an installation?","Yes — and it's complimentary. Lana analyzes your natural hair structure, density, and goals, then builds your personalized plan with exact pricing before you commit to anything."),
  ("What payment and booking system do you use?","Booking runs through Square Appointments — pick a date and service online. The consultation confirms your installation plan and timing."),
  ("Is parking available at the Burbank studio?","Yes, street parking is available near the studio on N Glenoaks Blvd.")]),
"hair-extensions-glendale": dict(city="Glendale",
 title="Hair Extensions Near Glendale, CA | K-Tip Specialist 10 Min Away",
 desc="Luxury K-Tip & BIO tape hair extensions 10 minutes from Glendale, CA. Slavic hair, zero-damage protocol by Lana. Private Burbank studio — free consultation.",
 h1="Hair Extensions for Glendale, California",
 eyebrow="10 Minutes from N Brand Blvd",
 lead="A 10-minute drive from the Brand Boulevard corridor brings you to a private Burbank studio where extensions are architected, not just installed.",
 img="/photos/g4.jpg", alt="Luxury K-Tip hair extensions for Glendale client, Culture of Extensions studio",
 local=["Glendale is our closest neighboring city — clients from the Americana area, Adams Hill, Rossmoyne, and Montrose reach the studio in about 10 minutes via Glenoaks or San Fernando Blvd.",
 "Rather than fitting you into a salon chair between other appointments, the studio model is different: one client at a time, a structural analysis of your natural hair first, and a personalized plan with exact pricing before anything is installed."],
 checks=["10 minutes from Brand Blvd & the Americana","Private one-client-at-a-time studio format","K-Tip micro-capsule & BIO tape in Slavic hair","Complimentary consultation with exact pricing"],
 faq=[("How far is the studio from central Glendale?","About 10 minutes by car from the N Brand Blvd area — the studio is at 2119 N Glenoaks Blvd in Burbank, just across the city line."),
  ("Why drive to Burbank instead of a Glendale salon?","Specialization. Culture of Extensions does one thing: premium hair extensions in Slavic and European hair. The methodology — structural analysis, zero-damage placement, invisible blending — is the result of 14+ years and 2,500+ transformations."),
  ("What extension methods are available?","Signature K-Tip micro-capsule (from $700), BIO tape with keratin toning (from $500), targeted volume work (from $400), and full length transformations in Slavic hair (from $1,000)."),
  ("Do you take clients with previous bad extension experiences?","Very often. Restoring hair after poor installations is part of the practice — the consultation includes an honest assessment of your hair's current condition and a recovery-first plan."),
  ("How do I book from Glendale?","Book the complimentary consultation online via Square Appointments — pick a date, and Lana takes it from there.")]),
"hair-extensions-studio-city": dict(city="Studio City",
 title="Hair Extensions Near Studio City, CA | Luxury K-Tip 15 Min Away",
 desc="Premium K-Tip & Slavic hair extensions 15 minutes from Studio City via the 101/134. Private Burbank studio by Lana — invisible artistry, free consultation.",
 h1="Hair Extensions for Studio City",
 eyebrow="15 Minutes via Ventura Blvd / 134",
 lead="For clients along Ventura Boulevard who expect camera-ready, undetectable results — a private studio 15 minutes away where invisibility is the standard.",
 img="/photos/g6.jpg", alt="Invisible hair extension blending for Studio City client, camera-ready result",
 local=["Studio City clients — many working in front of cameras or in the industry around the studios — come to us for one reason: extensions that remain a secret. Texture, porosity, and movement are matched so precisely that even hairdressers can't find the transition.",
 "The drive is simple: Ventura Blvd to the 134 or over Barham, about 15 minutes to our private Burbank studio. Appointments are unhurried and one-on-one — no salon floor, no audience."],
 checks=["Camera-ready, undetectable blending","15 minutes from Ventura Blvd via the 134","100% Slavic & European remy hair","Private one-on-one appointments"],
 faq=[("Are extensions detectable on camera or in HD?","Not when architected correctly. Micro-capsules are placed following your natural fall and the hair is blended across three color zones — the result holds up in HD, on set, and in person."),
  ("How long does an installation take?","Depending on the plan — from a couple of hours for targeted volume to several hours for a full transformation with finishing cut. Exact timing is set with your personalized plan."),
  ("Can extensions be styled with heat?","Yes — 100% natural Slavic and European remy hair styles like your own. You leave with a personalized care guide covering heat, washing, and maintenance."),
  ("What does parking and access look like?","Street parking near the studio at 2119 N Glenoaks Blvd in Burbank. The studio is private and appointment-only."),
  ("How quickly can I get an appointment?","Lana works with a select number of clients each month. Book the complimentary consultation online — installation dates are planned there.")]),
"hair-extensions-toluca-lake": dict(city="Toluca Lake",
 title="Hair Extensions Near Toluca Lake, CA | Private Studio 5 Min Away",
 desc="Luxury private hair extension studio 5 minutes from Toluca Lake. K-Tip & BIO tape in Slavic hair by Lana — discreet, appointment-only. Free consultation.",
 h1="Hair Extensions for Toluca Lake",
 eyebrow="5 Minutes · Adjacent to Toluca Lake",
 lead="Our studio sits five minutes from Toluca Lake — a discreet, appointment-only space built around privacy and unhurried, individual work.",
 img="/photos/g1.jpg", alt="Discreet luxury hair extension appointment near Toluca Lake",
 local=["Toluca Lake is effectively our neighborhood — the studio on N Glenoaks Blvd is a five-minute drive from Riverside Drive. For clients who value discretion, the format matters: private studio, one client at a time, no walk-ins.",
 "Every appointment follows the same architecture: structural analysis of your natural hair, a personalized plan with exact pricing, meticulous installation, and a care protocol with direct access to Lana between appointments."],
 checks=["5 minutes from Riverside Drive","Discreet, private, appointment-only format","Zero-damage protocol on every installation","Personalized care guide & direct access to Lana"],
 faq=[("How close is the studio to Toluca Lake?","Five minutes — the studio is at 2119 N Glenoaks Blvd in Burbank, adjacent to the Toluca Lake area."),
  ("Is the studio private?","Completely. One client at a time, by appointment only. Many clients choose us specifically for the discretion of the format."),
  ("Which method should I choose?","That's what the complimentary consultation answers. Lana analyzes your hair structure, density, and lifestyle, then recommends K-Tip, BIO tape, volume work, or a hybrid plan — with exact pricing."),
  ("What hair do you use?","Only 100% Slavic and European remy hair — naturally fine, soft, and color-matched across roots, mid-lengths, and ends."),
  ("How do I maintain extensions between appointments?","You leave with a personalized care guide and maintenance schedule, plus direct access to Lana for questions between appointments.")]),
"hair-extensions-pasadena": dict(city="Pasadena",
 title="Hair Extensions Near Pasadena, CA | Slavic Hair Specialist",
 desc="Premium Slavic hair extensions 25 minutes from Old Town Pasadena via the 134. K-Tip & BIO tape by Lana, Burbank private studio. Free consultation.",
 h1="Hair Extensions for Pasadena",
 eyebrow="25 Minutes via the 134 Freeway",
 lead="Pasadena clients take the 134 west for one thing they can't find closer: a specialist studio working exclusively in premium Slavic hair with a zero-damage methodology.",
 img="/photos/g3.jpg", alt="Premium Slavic hair extensions for Pasadena client, natural blending result",
 local=["From Old Town or Madison Heights, the drive west on the 134 takes about 25 minutes — and clients tell us it's the difference between a salon service and a specialist practice. Culture of Extensions does one discipline at the highest standard.",
 "The methodology is the draw: structural analysis before any commitment, micro-capsule placement mapped to your density, 100% Slavic hair blended across three color zones, and education so the result lives beyond the appointment."],
 checks=["Specialist practice — extensions only, nothing else","100% Slavic & European remy hair","Structural analysis & exact pricing before commitment","Education and care protocol included"],
 faq=[("Is it worth driving from Pasadena?","Clients who want specialist-level work think so. The studio works exclusively in premium hair extensions — a single discipline refined across 14+ years and 2,500+ transformations."),
  ("How long is the drive from Pasadena?","About 25 minutes from the Old Town area via the 134 freeway to our Burbank studio at 2119 N Glenoaks Blvd."),
  ("What makes Slavic hair different?","It is naturally fine, soft, and light with an intact cuticle — the closest structural match to most natural hair, and the only hair we install."),
  ("Can I get everything done in one visit?","The complimentary consultation comes first — analysis, plan, exact pricing. Installation is scheduled separately so the right hair is prepared and color-matched for you."),
  ("Do you offer maintenance for extensions installed elsewhere?","Case by case — book a consultation and Lana will assess the current installation honestly, including whether it can be maintained or should be redone safely.")]),
"hair-extensions-los-angeles": dict(city="Los Angeles",
 title="Luxury Hair Extensions in Los Angeles | K-Tip & Slavic Hair by Lana",
 desc="Luxury K-Tip & Slavic hair extensions for Los Angeles — Hollywood, WeHo & beyond. Private Burbank studio by Lana, 2,500+ transformations. Free consultation.",
 h1="Luxury Hair Extensions in Los Angeles",
 eyebrow="20 Minutes from Hollywood / WeHo",
 lead="Los Angeles has hundreds of salons that offer extensions among dozens of services. Culture of Extensions offers one discipline, architected to the highest standard — 20 minutes from Hollywood.",
 img="/photos/g5.jpg", alt="Luxury hair extensions Los Angeles — full transformation by Culture of Extensions",
 local=["Clients reach the Burbank studio from Hollywood, West Hollywood, Los Feliz, Silver Lake, and the Westside — most within 20–30 minutes via the 101 or Barham. What they come for is specialization: K-Tip micro-capsule and BIO tape installations in 100% Slavic and European hair, one client at a time.",
 "Every transformation follows the Culture of Extensions methodology: structural analysis of your natural hair, a personalized plan with exact pricing, meticulous unhurried installation, and education so the result lasts. Where modern goddesses are born — by Lana, Svitlana Levenets, 14+ years, 2,500+ transformations."],
 checks=["Serving Hollywood, WeHo, Los Feliz, Silver Lake & beyond","Signature K-Tip micro-capsule method","100% Slavic & European remy hair only","Complimentary private consultation · EN / ES / RU"],
 faq=[("Who is the best hair extension specialist in Los Angeles?","We'll let the work answer that — Lana (Svitlana Levenets) has spent 14+ years and 2,500+ transformations refining a methodology built on structural analysis, zero-damage placement, and invisible blending. Book a complimentary consultation and judge the plan she builds for you."),
  ("How much do luxury hair extensions cost in Los Angeles?","At Culture of Extensions: volume work from $400, BIO tape from $500, signature K-Tip from $700, and full Slavic-hair length transformations from $1,000 — with exact pricing set in your personalized plan."),
  ("Where is the studio?","2119 N Glenoaks Blvd in Burbank — about 20 minutes from Hollywood and West Hollywood. Private, appointment-only."),
  ("What languages are consultations available in?","English, Spanish, and Russian."),
  ("What is the first step?","A complimentary consultation. Lana analyzes your natural hair structure, density, and goals, then architects your personalized plan — method, hair, timeline, and exact price — before you commit.")]),
}

for slug, d in city_data.items():
    body = block(f"Why {d['city']} Clients Choose Culture of Extensions", d["local"], d["checks"])
    htm = page(slug, d["title"], d["desc"], d["h1"], d["eyebrow"], d["lead"],
               body, d["faq"], d["img"], d["alt"], city_schema(d["city"], slug, d["desc"]))
    open(f"{slug}.html","w").write(htm)
    pages_written.append(slug)
print("All pages:", len(pages_written))
