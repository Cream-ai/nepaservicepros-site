import csv,re
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
rows=[r for f in ['data/prosgrade_raw.csv','data/prosgrade_raw2.csv'] for r in csv.DictReader(open(f)) if r['state'] in('PA','Pennsylvania')]
catmap={'plumbing/HVAC':'Plumbing','HVAC':'HVAC','roofing':'Roofing','electrical':'Electrical','dentist':None}
names={slug(r['name']) for r in rows}
for r in csv.DictReader(open('../nepafound/leads/nepa-leads-50.csv')):
    c=r['category'].lower()
    t=('Plumbing' if 'plumb' in c else 'HVAC' if 'hvac' in c else 'Roofing' if 'roof' in c else 'Electrical' if 'electr' in c else 'Landscaping' if 'landsc' in c or 'lawn' in c else 'Painting' if 'paint' in c else 'Pest Control' if 'pest' in c else 'Remodeling' if 'remodel' in c or 'contract' in c else None)
    if not t or slug(r['business']) in names: continue
    names.add(slug(r['business']))
    rows.append(dict(name=r['business'],trade=t,town=r['town'],state='PA',zip='',phone='',website=r['website'],listed_city='',source='business website (public)'))
out=[];seen=set()
for r in rows:
    s=slug(r['name']);
    if s in seen: s=slug(r['name']+'-'+r['trade'])
    if s in seen: continue
    seen.add(s)
    out.append(dict(slug=s,name=r['name'].strip(),trade=r['trade'],town=r['town'].strip() or r['listed_city'].title(),zip=r['zip'],phone=r['phone'],website=r['website'],source=r['source'],tier='free',claimed='no',featured='no'))
w=csv.DictWriter(open('data/businesses.csv','w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
import collections;print(len(out),collections.Counter(o['trade'] for o in out))
