import re,json,subprocess,time,csv
T0={'plumbers':'Plumbing','hvac':'HVAC','roofers':'Roofing','electricians':'Electrical','painters':'Painting','landscapers':'Landscaping','pest-control':'Pest Control'}
T={'concrete':'Concrete','flooring':'Flooring','garage-doors':'Garage Doors','renovations':'Remodeling','windows':'Windows & Doors','locksmiths':'Locksmith','movers':'Moving','home-builders':'Home Builders','solar':'Solar'}
C=['scranton','wilkes-barre']
def get(u):
    time.sleep(0.4)
    return subprocess.run(['curl','-sL','-m','20','-A','Mozilla/5.0 (NEPAServicePros directory seed)',u],capture_output=True,text=True).stdout
def lds(h):
    o=[]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try:o.append(json.loads(b))
        except:pass
    return o
seen={};rows=[]
for t,tn in T.items():
  for c in C:
    for d in lds(get(f'https://prosgrade.com/{t}/{c}')):
      if d.get('@type')!='ItemList':continue
      for it in d['itemListElement']:
        u=it['url']
        if u in seen:continue
        seen[u]=1
        for p in lds(get(u)):
          if 'telephone' in p or 'address' in p:
            a=p.get('address',{});sa=[s for s in p.get('sameAs',[]) if not re.search(r'facebook|instagram|yelp|google|bbb|linkedin|angi|houzz|nextdoor|thumbtack',s)]
            rows.append(dict(name=p.get('name',it['name']),trade=tn,town=a.get('addressLocality',''),state=a.get('addressRegion','PA'),zip=a.get('postalCode',''),phone=p.get('telephone',''),website=(sa[0] if sa else ''),listed_city=c,source='prosgrade.com (public listing)'))
            break
    print(t,c,len(rows),flush=True)
k=set();out=[]
for r in rows:
  key=(r['name'].lower(),r['trade'])
  if key in k:continue
  k.add(key);out.append(r)
w=csv.DictWriter(open('data/prosgrade_raw2.csv','w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print('total',len(out))
