# NEPA Service Pros (business #4): vetted home-services directory + weekly newsletter for NE Pennsylvania

Owner: Interregnum Ventures LLC. Approved by Joel on 2026-10-15. Status: spec only. Nothing has been bought or sent.
Stack: GitHub Pages (Cream-ai/nepa-directory-site), Formspree, Stripe Payment Links, Porkbun DNS. It runs Grok-only, with no local models until the workflow is proven.
Feeds NEPA Found: every listed business gets a free AI-visibility check, and the "Claim/Upgrade" flow cross-sells the NEPA Found Basic plan and the $149 sprint.

## 1. Category choice (evidence, gathered 2026-10-15)
| Candidate | Demand signal | Existing NEPA directories, weakness | Who pays | Verdict |
|---|---|---|---|---|
| **Home services/contractors** (plumbing, HVAC, roofing, remodel, gutters, electric, paving, tree) | Google autocomplete includes "plumbers scranton pa prices", "emergency plumber scranton pa", "plumbers scranton pa residential", "roofing wilkes barre pa", "nepa contractors bathroom". There are recurring r/Scranton threads asking for contractors: https://www.reddit.com/r/Scranton/comments/1p07up7/ , https://www.reddit.com/r/Scranton/comments/1plbco6/ , https://www.reddit.com/r/Scranton/comments/1cypewc/ . Users complain that "anyone good is booked out a year" and that nobody shows up, so a trust/availability gap exists. | Chamber directories (https://weblink.scrantonchamber.com/search , https://business.wilkeschamber.com/list ) are members-only, unranked and carry no reviews or availability. Angi, Thumbtack and HomeAdvisor sell pay-per-lead, which contractors resent. nepahomepros.com is already registered, so a competitor or squatter likely exists; check its content before launch. | Contractors: a single job is worth $500 to $20k, so a $29 to $49/mo featured listing is easy to justify. They are also the same ICP as NEPA Found. | **Pick** |
| Events | DiscoverNEPA already runs a strong regional events calendar (https://discovernepa.com/ ). | Well-funded incumbent with free listings | Event organizers have small budgets | No |
| Restaurants | High demand, but Google Maps, Yelp and DiscoverNEPA "Where to Eat" (https://discovernepa.com/things-to-do/where-to-eat/ ) dominate | Saturated | Thin margins; restaurants rarely pay for listings | No |
| Wedding vendors | Good willingness to pay | DiscoverNEPA wedding guide (https://discovernepa.com/plan-a-wedding-in-nepa ), The Knot, WeddingWire | Vendors pay, but The Knot owns search | Phase-2 vertical at most |
| Childcare | Real need | PA state lists (Childcare Works/COMPASS) are free and authoritative | Low ability to pay, plus regulatory and trust risk | No |

Why home services wins: it has the clearest paying buyer, it overlaps 100% with NEPA Found's lead list and pitch, and it has a defensible "no pay-per-lead, no phone spam" angle against Angi. Demand evidence is qualitative because we have no paid keyword tool. Before launch, validate volume with Google Keyword Planner (free with an Ads account) or Search Console impressions after 30 days.

## 2. Domain (Porkbun checkDomain API, 2026-10-15, check only)
- **Primary: nepaservicepros.com**: AVAILABLE, $11.08
- Backup 1: nepatradespros.com: AVAILABLE, $11.08
- Backup 2: pronepa.com: AVAILABLE, $11.08
- Taken: nepapros.com, nepahomepros.com
Purchase needs Joel's approval (about $11/yr).

## 3. Data sources and automatic updates
- **Seed** (about 300 businesses across 10 trades × 8 towns: Scranton, Wilkes-Barre, Kingston, Pittston, Hazleton, Clarks Summit, Dunmore, Dallas). Sources: the existing nepafound/leads CSV, public chamber directory pages, business websites, the PA Home Improvement Contractor registry (PA Attorney General HIC lookup, public), and BBB pages. Record only public facts: name, trade, town, website, public email, HIC#, and a link to the Google profile. Never copy review text.
- **Repo layout:** `data/businesses.csv` is the single source of truth. `build.py` renders static pages with Jinja2 into `/docs`.
- **GitHub Actions cron:**
  - Weekly (Mon 6 AM ET): run `check_links.py` (URL is 200, site HTTPS, email MX valid), flag stale rows (`last_verified` older than 120 days), and open a GitHub issue listing them.
  - Nightly: rebuild and deploy.
  - Monthly: run the NEPA Found `make_report.py` against a batch of listings and save the AI-visibility status as the lead feed for NEPA Found.
- **Formspree:** the "Add / claim / correct your listing" form and the "Request a recommendation" form for homeowners. A script pulls submissions via the Formspree API (key in /workspace/ventures/secrets/formspree.txt) into `data/submissions/`. Grok reviews them, then commits. Nothing auto-publishes unverified.
- **Paid status:** a Stripe webhook isn't possible on Pages, so `sync_stripe.py` (daily cron, run on the box with the restricted read key) marks `featured=true` from active subscriptions.

## 4. Site structure and SEO
- `/` hero: "Vetted NEPA home-service pros. No lead fees, no phone spam." Search by trade and town.
- `/[trade]/` (10 pages) and `/[trade]/[town]/` (80 programmatic pages, each with a unique intro, the PA HIC note, a price-range FAQ such as "How much does a plumber cost in Scranton?" to target the autocomplete "prices" queries, and a FAQPage schema).
- `/pro/[slug]/` business profiles with LocalBusiness JSON-LD, a HIC# badge and a "Featured" badge.
- `/guides/` 6 evergreen guides: hiring a contractor in PA (the HIC law), roof replacement cost NEPA, emergency plumber checklist, and others.
- `/for-pros/` pricing and claim; `/newsletter/`; sitemap.xml; robots; Search Console plus Bing Webmaster at launch. Rule: no thin pages, so a town page only goes live with at least 3 real listings.

## 5. Weekly newsletter: "NEPA Home Weekly"
- Tool: **Buttondown** (free up to 100 subscribers, Markdown, API) or Beehiiv free (up to 2,500 subscribers, built-in ad network). **Choose Beehiiv** for its free tier size and sponsor tools. The CAN-SPAM address is 91 Price Street Fl 2, Kingston, PA 18704.
- Format (Thursday): 1 seasonal home tip (frozen pipes, ice dams), 3 featured pros, 1 "new to the directory", 1 sponsor slot, and local permit/utility news. Grok drafts it and Joel approves each send.
- Growth: signup box on every page; posting in r/Scranton and r/wilkesbarre only as genuinely useful guides, following sub rules with mod OK; Facebook NEPA community groups with Joel's approval.

## 6. Pricing
- Free basic listing: always free, which builds inventory.
- **Featured Pro, $29/mo** (or $290/yr): top of trade and town pages, badge, photos, a newsletter mention each month, and a free AI-visibility report.
- **Founding Sponsor, $49/mo, locked for life, first 10 only**: exclusive per trade+town, plus everything in Featured.
- **Newsletter sponsor:** $25/issue at launch, $50 once there are 1,000+ subscribers.
- **Bundle:** NEPA Found Basic ($49) plus Featured = $59/mo.
- Path to $100/mo: **4 Featured ($116)** or **2 Founding Sponsors + 1 Featured ($127)**. Stripe needs 4 new Payment Links (Featured monthly, Featured annual, Founding Sponsor, Newsletter slot). Creating them needs Joel's OK.

## 7. 60-day $100/mo kill rule
SEO won't produce money in 60 days, so revenue comes from direct online sales of founding spots, and SEO is the long-term bet.
- **Day 0 (launch):** site live with at least 150 listings across 10 trades. Pick 40 high-review contractors with public emails or contact forms. Each gets an email (Joel-approved batch) saying "You're listed free on NEPA Service Pros; here's your free AI-visibility finding; 10 Founding spots at $49/mo locked." Use contact forms too. Also send a Facebook/LinkedIn DM where Joel approves. No phone.
- **Day 14:** second touch to non-responders. Second batch of 40.
- **Day 30 milestone:** at least 1 paying customer ($29 to $49), 100 newsletter subscribers, and 300 listings. If there are 0 sales after 80 contacts, test a $1 first-month Founding offer or the $59 bundle.
- **Day 45:** third batch. Offer the newsletter sponsor slot to a local supplier (lumber yard, plumbing supply).
- **Day 60 milestone:** at least $100 MRR, for example 2 Founding + 1 Featured. If it's under $100, kill it, **unless** NEPA Found closed at least 1 client sourced from the directory. In that case Joel decides whether to count combined revenue as a lead engine. (Proposal only; Joel decides.)
- Costs: domain about $11/yr; everything else free. The downside is tiny.

## 8. Build checklist
- [ ] Joel: approve the domain buy (nepaservicepros.com, $11.08) and the 4 Stripe Payment Links
- [ ] Create repo Cream-ai/nepa-directory-site, Pages + custom domain + HTTPS, Porkbun DNS (A/CNAME)
- [ ] `businesses.csv` schema plus a 150-row seed from the leads CSV and public sources
- [ ] `build.py` (Jinja2): home, trade, trade-town, profile, guides, for-pros, schema, sitemap
- [ ] Formspree forms: claim/add/correct, homeowner request, newsletter fallback
- [ ] GitHub Actions: nightly build, weekly link and staleness check, issue creation
- [ ] `sync_stripe.py` and `pull_formspree.py` on the box
- [ ] Beehiiv account, first 2 issues drafted
- [ ] Search Console plus Bing, sitemap submitted
- [ ] Outreach batch 1 drafted (40) for Joel's approval, shared with the NEPA Found sequence to avoid double-emailing
- [ ] Dashboard row in LAUNCH-STATUS.md: MRR, listings, subscribers, day count
