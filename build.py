#!/usr/bin/env python3
"""Build NEPA Service Pros static site from data/businesses.csv into docs/."""
import csv, os, re, json, shutil, html, datetime
from collections import defaultdict
D='https://nepaservicepros.com'
FORM='https://formspree.io/f/xeaevzga'
L={'featured':'https://buy.stripe.com/3cI14m81E32NeLQ2El4Ja0b','founding':'https://buy.stripe.com/fZu8wOdlY6eZdHMbaR4Ja0c',
   'slot':'https://buy.stripe.com/3cI4gy81EavfdHM6UB4Ja0d','bundle':'https://buy.stripe.com/aFa7sKdlY6eZ8ns0wd4Ja0e'}
e=html.escape
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
R=list(csv.DictReader(open('data/businesses.csv')))
OUT='docs'
if os.path.isdir(OUT): shutil.rmtree(OUT)
pages=[]
CSS="""body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1d2433;line-height:1.55;background:#f7f8fa}
a{color:#0b5cad}header{background:#12324f;color:#fff;padding:14px 20px}header a{color:#fff;text-decoration:none;margin-right:16px}
.logo{font-weight:800;font-size:1.15em}.wrap{max-width:1000px;margin:0 auto;padding:20px}.hero{background:#fff;border-radius:12px;padding:28px;margin:18px 0}
h1{margin:.2em 0}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}.card{background:#fff;border:1px solid #e3e7ee;border-radius:10px;padding:14px}
.card h3{margin:.1em 0 .3em;font-size:1.05em}.muted{color:#5b6475;font-size:.92em}.btn{display:inline-block;background:#e8742b;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600;border:0;cursor:pointer;font-size:1em}
.tier{background:#fff;border:2px solid #e3e7ee;border-radius:12px;padding:18px}.tier.hot{border-color:#e8742b}.price{font-size:1.6em;font-weight:800}
input,textarea,select{width:100%;padding:9px;margin:4px 0 10px;border:1px solid #c9d0db;border-radius:6px;box-sizing:border-box;font:inherit}
footer{color:#5b6475;font-size:.85em;padding:30px 20px;text-align:center}.pill{display:inline-block;background:#eef3f9;border-radius:20px;padding:4px 10px;margin:3px;font-size:.9em;text-decoration:none}"""
def page(path,title,desc,body,ld=None):
    url=D+'/'+path
    lds=f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ''
    h=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><link rel="stylesheet" href="/style.css">{lds}</head><body>
<header><a class="logo" href="/">NEPA Service Pros</a><a href="/#trades">Find a pro</a><a href="/newsletter/">Newsletter</a><a href="/for-pros/">For pros</a></header>
<div class="wrap">{body}</div>
<footer>NEPA Service Pros is a free directory of Northeastern Pennsylvania home-service businesses. Listings are compiled from public business information; we do not copy reviews. Is this your business? <a href="/claim/">Claim or update it free</a>.<br>
Interregnum Ventures LLC · 91 Price Street Fl 2, Kingston, PA 18704 · <a href="/privacy/">Privacy</a></footer></body></html>"""
    p=os.path.join(OUT,path); os.makedirs(p,exist_ok=True); open(os.path.join(p,'index.html'),'w').write(h); pages.append(url)
def card(b):
    tel=f'<br><a href="tel:{re.sub(r"[^0-9+]","",b["phone"])}">{e(b["phone"])}</a>' if b['phone'] else ''
    feat=' ★ Featured' if b.get('featured')=='yes' else ''
    return f'<div class="card"><h3><a href="/pro/{b["slug"]}/">{e(b["name"])}</a>{feat}</h3><div class="muted">{e(b["trade"])} · {e(b["town"])}, PA</div>{tel}</div>'
def sortk(b): return (b.get('featured')!='yes', b['name'].lower())
bytrade=defaultdict(list); bytt=defaultdict(list); bytown=defaultdict(list)
for b in R: bytrade[b['trade']].append(b); bytt[(b['trade'],b['town'])].append(b); bytown[b['town']].append(b)
os.makedirs(OUT); open(f'{OUT}/style.css','w').write(CSS)
# home
tl=''.join(f'<a class="pill" href="/{slug(t)}/">{e(t)} ({len(v)})</a>' for t,v in sorted(bytrade.items()))
towns=sorted([t for t,v in bytown.items() if len(v)>=3],key=lambda t:-len(bytown[t]))
tw=''.join(f'<a class="pill" href="/town/{slug(t)}/">{e(t)} ({len(bytown[t])})</a>' for t in towns)
page('','NEPA Service Pros: Local home-service pros in Scranton, Wilkes-Barre & NEPA','Find plumbers, roofers, HVAC, electricians and more across Northeastern PA. Free directory. No lead fees, no phone spam.',
f"""<div class="hero"><h1>Vetted NEPA home-service pros.</h1><p style="font-size:1.2em">No lead fees, no phone spam. Call the business directly.</p>
<p class="muted">{len(R)} local businesses across Lackawanna &amp; Luzerne counties. Scranton, Wilkes-Barre, Kingston, Dunmore and surrounding towns.</p></div>
<h2 id="trades">Browse by trade</h2><p>{tl}</p><h2>Browse by town</h2><p>{tw}</p>
<div class="hero"><h2>Homeowner newsletter</h2><p>One short email a month: seasonal NEPA home tips and new local pros. No spam.</p><a class="btn" href="/newsletter/">Subscribe free</a></div>""",
{"@context":"https://schema.org","@type":"WebSite","name":"NEPA Service Pros","url":D+'/'})
# trade pages
for t,v in bytrade.items():
    ts=sorted({b['town'] for b in v})
    links=''.join(f'<a class="pill" href="/{slug(t)}/{slug(x)}/">{e(t)} in {e(x)}</a>' for x in ts if len(bytt[(t,x)])>=3)
    page(slug(t)+'/',f'{t} in Northeastern PA | NEPA Service Pros',f'{len(v)} {t.lower()} businesses serving Scranton, Wilkes-Barre and NEPA. Phone numbers and websites, no lead fees.',
      f'<h1>{e(t)} in Northeastern PA</h1><p class="muted">{len(v)} local businesses. Contact them directly. We never sell your info.</p><p>{links}</p><div class="grid">{"".join(card(b) for b in sorted(v,key=sortk))}</div>')
for (t,x),v in bytt.items():
    if len(v)<3: continue
    page(f'{slug(t)}/{slug(x)}/',f'{t} in {x}, PA | NEPA Service Pros',f'{len(v)} {t.lower()} businesses in {x}, PA with phone numbers and websites.',
      f'<p><a href="/{slug(t)}/">← All {e(t)}</a></p><h1>{e(t)} in {e(x)}, PA</h1><div class="grid">{"".join(card(b) for b in sorted(v,key=sortk))}</div>')
for x in towns:
    v=bytown[x]
    page(f'town/{slug(x)}/',f'Home-service pros in {x}, PA | NEPA Service Pros',f'{len(v)} plumbers, roofers, HVAC and other home-service businesses in {x}, PA.',
      f'<h1>Home-service pros in {e(x)}, PA</h1><div class="grid">{"".join(card(b) for b in sorted(v,key=lambda b:(b["trade"],)+sortk(b)))}</div>')
# profiles
for b in R:
    ld={"@context":"https://schema.org","@type":"LocalBusiness","name":b['name'],"address":{"@type":"PostalAddress","addressLocality":b['town'],"addressRegion":"PA","postalCode":b['zip']},"url":D+f'/pro/{b["slug"]}/'}
    if b['phone']: ld['telephone']=b['phone']
    if b['website']: ld['sameAs']=[b['website']]
    web=f'<p>Website: <a href="{e(b["website"])}" rel="nofollow noopener">{e(re.sub(r"^https?://(www\.)?","",b["website"]).rstrip("/"))}</a></p>' if b['website'] else ''
    tel=f'<p>Phone: <a href="tel:{re.sub(r"[^0-9+]","",b["phone"])}">{e(b["phone"])}</a></p>' if b['phone'] else ''
    page(f'pro/{b["slug"]}/',f'{b["name"]}: {b["trade"]} in {b["town"]}, PA',f'{b["name"]} is a {b["trade"].lower()} business in {b["town"]}, PA. Phone, website and service info.',
      f'<p><a href="/{slug(b["trade"])}/">← {e(b["trade"])}</a></p><div class="hero"><h1>{e(b["name"])}</h1><p class="muted">{e(b["trade"])} · {e(b["town"])}, PA {e(b["zip"])}</p>{tel}{web}</div>'
      f'<div class="card"><b>Is this your business?</b> Claim it free to correct details, add services, hours and photos. <a href="/claim/?b={b["slug"]}">Claim / update this listing</a></div>'
      f'<p class="muted">Basic listing compiled from public business information. Unclaimed.</p>',ld)
# claim
page('claim/','Claim or update your free listing | NEPA Service Pros','Claim, correct or remove your NEPA Service Pros listing. Free.',
f"""<h1>Claim or update your listing (free)</h1><p>Correct your details, add services and hours, or ask us to remove the listing. Free forever. We will not call you.</p>
<form action="{FORM}" method="POST"><input type="hidden" name="_subject" value="NEPA Service Pros: claim/update"><input type="hidden" name="form" value="nsp-claim">
<label>Listing (slug or business name)</label><input name="listing" id="lst" required><label>Your name</label><input name="name" required>
<label>Email</label><input type="email" name="email" required><label>Request</label><select name="request"><option>Claim and update</option><option>Correct details</option><option>Add a new business</option><option>Remove my listing</option></select>
<label>Details (phone, website, services, towns served)</label><textarea name="details" rows="5"></textarea><button class="btn" type="submit">Send</button></form>
<script>var b=new URLSearchParams(location.search).get('b');if(b)document.getElementById('lst').value=b;</script>""")
page('newsletter/','NEPA homeowner newsletter | NEPA Service Pros','A free monthly email for NEPA homeowners with seasonal tips and new local pros.',
f"""<h1>The NEPA Homeowner newsletter</h1><p>One short email a month: seasonal maintenance for NEPA weather (freeze-ups, ice dams, sump pumps), plus newly listed local pros. Unsubscribe anytime.</p>
<form action="{FORM}" method="POST"><input type="hidden" name="_subject" value="NEPA Service Pros: newsletter signup"><input type="hidden" name="form" value="nsp-newsletter">
<label>Email</label><input type="email" name="email" required><label>Town (optional)</label><input name="town"><button class="btn" type="submit">Subscribe free</button></form>""")
page('for-pros/','For pros: free listing, Featured Pro and sponsorships | NEPA Service Pros','Get found by NEPA homeowners. Free listing, no lead fees. Optional Featured Pro and sponsor placements.',
f"""<h1>For NEPA home-service pros</h1><p>Your basic listing is free and stays free. No lead fees and no shared leads. Homeowners call you directly. Optional upgrades:</p>
<div class="grid"><div class="tier"><h3>Free listing</h3><div class="price">$0</div><p>Name, phone, website, trade and town pages.</p><a class="btn" href="/claim/">Claim free</a></div>
<div class="tier hot"><h3>Featured Pro</h3><div class="price">$29/mo</div><p>Top of your trade and town pages, Featured badge, services, hours and photos.</p><a class="btn" href="{L['featured']}">Get featured</a></div>
<div class="tier"><h3>Founding Sponsor</h3><div class="price">$49/mo</div><p>Top placement across your trade site-wide plus a monthly newsletter mention. Only 10 spots.</p><a class="btn" href="{L['founding']}">Become a sponsor</a></div>
<div class="tier"><h3>Newsletter slot</h3><div class="price">$25</div><p>One sponsored spot in the homeowner newsletter. One-time.</p><a class="btn" href="{L['slot']}">Book a slot</a></div>
<div class="tier"><h3>NEPA Found bundle</h3><div class="price">$59/mo</div><p>Featured Pro plus <a href="https://nepafound.com">NEPA Found</a> monthly AI-search visibility monitoring.</p><a class="btn" href="{L['bundle']}">Get the bundle</a></div></div>
<p class="muted">Cancel anytime. Payments handled securely by Stripe. Questions? Use the <a href="/claim/">claim form</a>.</p>""")
page('privacy/','Privacy | NEPA Service Pros','Privacy policy.','<h1>Privacy</h1><p>We collect only what you submit through our forms (name, email, listing details) to update listings and send the newsletter you asked for. We do not sell data. Business listings use public business information; owners may correct or remove a listing anytime via the claim form.</p>')
today=datetime.date.today().isoformat()
open(f'{OUT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc><lastmod>{today}</lastmod></url>' for u in pages)+'</urlset>')
open(f'{OUT}/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {D}/sitemap.xml\n')
open(f'{OUT}/CNAME','w').write('nepaservicepros.com\n'); open(f'{OUT}/.nojekyll','w').write('')
print(len(R),'listings',len(pages),'pages')
