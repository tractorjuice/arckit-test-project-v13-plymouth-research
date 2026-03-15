# We Tracked 243 Plymouth Restaurants. Here's What We Found About Food, Hygiene, and the Data Nobody Looks At

*A data journalism investigation into what free public data reveals about a city's dining scene, and what it hides.*

> **By the numbers**
> 243 restaurants tracked | 2,625 menu items | 9,410 Trustpilot reviews | 486 Google reviews | 8 data sources | Total cost: £0

## 1. A Five-Star Kitchen You'd Never Go Back To

We started with a simple question: where should you eat in Plymouth? The answer, we assumed, would be straightforward. Find the restaurants with the best hygiene ratings. Cross-reference them with what customers actually think. Recommend the winners.

It took about fifteen minutes to realise that plan was broken.

We tracked 243 restaurants across Plymouth, scraped menus from 98 of them, and found 36 where we could directly compare food hygiene ratings with customer reviews. The result was a paradox. Restaurants with a perfect 5 out of 5 from the Food Standards Agency, meaning inspectors found their kitchens to be in excellent condition, averaged just 2.65 stars out of 5 on Trustpilot. That figure comes from 27 restaurants. The eight restaurants sitting at 4-star hygiene fared even worse, averaging 2.40 on Trustpilot.

A clean kitchen, it turns out, does not predict a good meal.

### The gap at its widest

The disconnect is sharpest among the big chains. Every one of the restaurants below passed its hygiene inspection with top marks. Every one of them has a Trustpilot rating that most businesses would consider a crisis.

Taco Bell Plymouth: FSA Hygiene 5, Trustpilot 1.66 (gap of 3.34)
Papa John's Plymouth: FSA Hygiene 5, Trustpilot 1.88 (gap of 3.12)
McDonald's Plymouth: FSA Hygiene 5, Trustpilot 1.89 (gap of 3.11)
Domino's Pizza Plymouth: FSA Hygiene 5, Trustpilot 1.95 (gap of 3.05)
Pizza Hut Plymouth: FSA Hygiene 5, Trustpilot 1.99 (gap of 3.01)
Burger King Plymouth: FSA Hygiene 5, Trustpilot 2.04 (gap of 2.96)

The best performers in our dataset are the ones you might expect: restaurants where a real chef is cooking real food to order. Rockfish Plymouth managed an FSA 5 alongside a Trustpilot score of 3.75. Not spectacular, but head and shoulders above the chains. Armado Lounge followed at 3.1 on Trustpilot, again with a perfect hygiene record (though, like the chains above, this rating reflects the Loungers group nationwide, not the Plymouth branch specifically).

### What it took to find out

Understanding why this disconnect exists required us to go far beyond a single spreadsheet. We ended up combining eight free, publicly available data sources: food hygiene inspections, customer reviews from two platforms, menu prices, company registration data, geographic deprivation indexes, licensing records, and commercial property valuations. Every source was free. None of them, on its own, told the whole story.

The journey of stitching those sources together turned out to reveal as much as the findings themselves. Matching a restaurant name in one database to the same restaurant in another sounds trivial until you try it. It is not trivial. It is, in fact, the hardest part of the entire project, and it taught us more about data quality than any textbook ever could.

## 2. What Your Money Buys

Before we get to the machinery behind the data, let us start with something tangible. What does ten pounds actually get you in Plymouth?

We extracted 2,625 menu items across 98 restaurants. Of those, 2,161 had valid prices we could analyse. The average item price across the entire dataset was £10.68, a number that conceals enormous variation.

### From fine dining to fast food

At the top end, Plymouth's fine dining and Michelin-associated restaurants averaged £24.38 per item. Wine bars and small plates venues came in at £22.36, though the "per item" framing matters here as small plates are designed to be ordered in multiples. Seafood and fish restaurants, a category with a substantial 123 items in our sample, averaged £11.21. Italian cuisine (195 items) sat at £9.74, and Japanese food (183 items) came in at a similar £9.53.

Drop down to the fast food tier and the average falls to £3.96. Bakeries were the most affordable category at £3.53 per item. In total, we identified more than 17 distinct cuisine categories across Plymouth's restaurant scene.

### The extremes and their asterisks

The most expensive meaningful item we found was the Àclèaf 4-Course Tasting Menu at £75.00, from Àclèaf at Boringdon Hall, one of Plymouth's fine dining destinations. That represents the kind of considered, high-end offering that sits at the opposite end of the spectrum from a £3.53 bakery item.

The raw maximum in our dataset was actually £153.00, attributed to a Pret A Manger "Classic Lunch Bundle." This is a multi-item meal deal, not a single dish, and it highlights how scraped data can mislead if you take it at face value. At the other end, the raw minimum was £0.03, almost certainly a parsing error where our price extraction code misidentified a piece of text as a price. We present both raw and cleaned figures throughout this article because transparency about data quality matters more than tidy numbers.

### What we could not measure

We had planned to include dietary analysis: how many items are vegetarian, vegan, or gluten-free, broken down by cuisine type. In practice, the HTML we scraped from restaurant websites did not yield reliable dietary tags. Some sites use icons, others use footnotes, many use nothing at all. We flag this as an honest gap in our analysis rather than guessing.

It is also worth noting that our data was collected in November 2025. Restaurant menus change, prices shift with inflation and supply costs, and we have no automated refresh mechanism. The figures here are a snapshot, not a live feed. They are accurate to a point in time, not to the moment you read this.

## 3. The Data Sources: Eight Ways to See a Restaurant

The foundation of this project is not a single dataset but eight separate ones, each offering a different lens on the same restaurants. We used no paid subscriptions, no premium APIs, and no proprietary databases. Everything here is available to anyone with an internet connection and some patience.

**FSA Food Hygiene Ratings** were our starting point and the most authoritative source in the stack. The Food Standards Agency publishes inspection data as an XML download under the Open Government Licence v3.0, making it free to use, share, and adapt. The Plymouth file covers 1,054 establishments, not just restaurants, but schools, hospitals, and takeaways too. We matched 202 of those to our restaurant database, giving us 83% coverage. Each entry provides a 0 to 5 star rating plus granular sub-scores for hygiene practice, structural condition, and management confidence. The limitation is temporal: a rating reflects what inspectors found on a single day, and that day could have been months or even years ago.

**Trustpilot Reviews** gave us the customer's voice, scraped directly from public review pages at no cost. Only 63 of our 243 restaurants, just 26%, have any Trustpilot presence at all. From those 63, we collected 9,410 reviews spanning twelve years, from late 2013 to November 2025. The coverage gap is the defining limitation here: nearly three-quarters of Plymouth's restaurants simply are not on Trustpilot. Compounding this, chain restaurant reviews on Trustpilot are company-wide rather than location-specific, so a one-star review about a branch in Glasgow can drag down the Plymouth score. We also lost access to at least one restaurant page mid-project when it returned a 404 error.

**Google Places API** offered the broadest coverage of any single source, reaching approximately 98% of our restaurants through its REST interface. Google provides a free tier with $200 per month in credit, more than sufficient for a research project of this scale. Each entry includes ratings, review counts, service options such as dine-in and delivery availability, vegetarian menus, business status, and GPS coordinates. The constraint is depth: the API returns a maximum of five reviews per restaurant, making it useful for ratings but thin on qualitative insight.

**Menu Web Scraping** was the most labour-intensive source. Using BeautifulSoup for static pages and Selenium for JavaScript-heavy sites, we parsed the actual menu pages of 98 Plymouth restaurants and extracted 2,625 individual menu items. This was free in monetary terms but expensive in engineering time, because every restaurant's website uses different HTML structure. Prices can be embedded in spans, divs, or plain text. Some are formatted with pound signs, others without. There is no automated refresh, so the data ages from the moment it is collected.

**Companies House** provided the corporate layer. The UK government's free API gave us company registration details, director names, and annual accounts, including turnover, profit-and-loss, and net assets, for 102 of our 243 restaurants, a 42% hit rate. The gap exists because sole traders and partnerships are not required to register at Companies House. Financial data from this source is always at least twelve months old, since companies file annually in arrears.

**ONS Geography** delivered the spatial and socioeconomic context. The Office for National Statistics publishes a free postcode directory that we downloaded and cross-referenced against every restaurant address. This gave us 100% coverage for ward, Lower Layer Super Output Area, parliamentary constituency, and Index of Multiple Deprivation, a composite measure of how deprived a neighbourhood is. The directory is updated quarterly, which is more than adequate for our purposes.

**Plymouth Licensing** data came from scraping the council's website. This source provides licensing hours and business categories, telling us which restaurants can serve alcohol and how late they can stay open. Coverage is partial and integration is still in progress. It represents the long tail of data work: useful in principle, fiddly in practice, and always one more cleaning step away from being truly ready.

**Business Rates (VOA)** data from the Valuation Office Agency rounds out our eight sources. This free public download provides rateable values for commercial properties, essentially a government estimate of what a premises would rent for on the open market. Rateable value serves as a rough proxy for premises size and commercial desirability. Like the licensing data, this source is still being integrated into our main database.

Six of these sources are fully operational. Two more are in progress. Every one of them is free. And none of them, taken alone, tells the whole story.

## 4. The Hard Part: Making Data Talk to Each Other

Collecting data from eight sources is straightforward compared to what comes next: making those sources agree on which restaurant is which. This is the problem of entity resolution, and it is deceptively difficult.

### The name problem

Consider this real example from our dataset. In our own restaurant database, the entry reads "Barbican Kitchen (Original)." On review sites, the same business appears as "Barbican Kitchen Brasserie." At Companies House, it is registered as "THE BARBICAN KITCHEN LTD."

Same restaurant. Three names. A human spots the match instantly. A computer, however, sees three strings of characters that do not match. One has a parenthetical qualifier, another adds "Brasserie," and the third has "THE" prepended and "LTD" appended. Multiply this across 243 restaurants and eight data sources, and you begin to see the scale of the problem.

### Teaching a computer to squint

We built a scoring algorithm that mimics the way a human would eyeball two entries and decide whether they refer to the same place. It works on a 100-point scale, broken into three components.

The first component is name similarity, worth up to 50 points. We strip away corporate suffixes like "LIMITED", "LTD", "PLC" and location markers like "(PLYMOUTH)", then measure how alike the remaining names are. "Barbican Kitchen" and "Barbican Kitchen Brasserie" score highly here because the core name is identical even though one version adds a descriptor.

The second component is the postcode match, worth 30 points. If two entries share exactly the same postcode, that is strong evidence they refer to the same physical location. Plymouth postcodes follow the PL pattern, and an exact match on something like PL1 2HJ is hard to dismiss as coincidence.

The third component is address similarity, worth up to 20 points. This measures how closely the street-level address details match: the road name, the building number, the neighbourhood. It catches cases where names diverge but the physical address confirms a match.

Any pair of records scoring 60 points or above is treated as a match. Anything below that threshold is flagged for manual review.

### The improvement that changed everything

Our first matching run, comparing 98 scraped restaurants against the FSA database, matched 49, exactly half. That felt disappointing until we investigated why the other half failed. The answer was not our algorithm. It was our data.

The FSA file we had downloaded was months old. Restaurants had opened, closed, and been re-inspected in the interim. When we downloaded a fresh copy of the FSA data and ran our matcher against the full universe of 243 restaurants, the match rate jumped to 202 out of 243, an 83% hit rate. The bottleneck was never our algorithm. It was stale source data.

### Keeping the data honest

Matching is only one piece of the quality puzzle. We built several safeguards into the pipeline to catch errors before they reach the dashboard.

At the point of ingestion, we validate incoming data against basic constraints. Prices must be positive numbers within a plausible range. Postcodes must match the expected UK format. Ratings must fall within the scale defined by their source: 0 to 5 for the FSA, 1 to 5 for Trustpilot and Google.

For deduplication, the database itself enforces uniqueness through composite indexes. If someone runs the Trustpilot scraper twice for the same restaurant, the second run cannot insert duplicate reviews. The database rejects them at the door.

For aggregation, we use database triggers that automatically recalculate average ratings and review counts every time a review is inserted or deleted. This means the dashboard always reflects the current state of the data without needing a separate batch process.

### What we got wrong

Transparency demands that we state what we know is imperfect. Some of our matches are probably wrong. When two restaurants have similar names and happen to share a postcode, not impossible in a city centre, the algorithm will match them even if they are different businesses. We have no systematic way to catch these false positives short of manual review.

The bigger limitation is coverage overlap. Only 36 of our 243 restaurants, just 15%, have data from both the FSA hygiene system and Trustpilot. That means the hygiene-versus-satisfaction analysis in Section 1 rests on a narrow foundation. Trustpilot coverage is the bottleneck, and unless more Plymouth restaurants establish Trustpilot profiles, it will remain one.

Finally, we have no audit trail for manual corrections. When a human overrides the algorithm to force or reject a match, that decision is not logged in a way that would let a future researcher understand why. This is a gap we intend to close, but have not yet.

## 5. Scraping Ethically in 2026

Web scraping has a reputation problem. Too many projects treat the open web as a resource to be strip-mined, hammering servers with rapid-fire requests, spoofing browser identities, ignoring the signals site owners put up to say "please don't." We decided early that if this project couldn't be done ethically, it wouldn't be done at all.

That decision shaped every technical choice we made.

### Asking permission first

Every URL we fetch is checked against the site's robots.txt file before we make the request. This is the most basic courtesy of automated web access, and one that many scrapers skip entirely. If a site says "don't crawl this path," we don't crawl it. If robots.txt can't be reached due to a network error, we default to deny. The safe assumption is that we don't have permission until we can confirm otherwise.

Where a robots.txt file includes a Crawl-delay directive, we respect that too. If a site owner says "wait ten seconds between requests," that instruction overrides our own settings.

### Slowing down on purpose

We built a 5-second minimum delay between requests to the same domain, enforced programmatically, not as a suggestion, but as a hard constraint. For Trustpilot specifically, we wait 2.5 seconds between pagination pages and 5 seconds between restaurants. The implementation is thread-safe, which means that even if multiple parts of the system try to fetch from the same domain simultaneously, only one request goes through at a time.

This makes the scraper slow. Collecting 9,410 Trustpilot reviews across 63 restaurants took hours, not minutes. We considered that an acceptable trade-off.

### No disguises

Our User-Agent string identifies exactly who we are: `PlymouthResearchMenuScraper/1.0 (+https://plymouthresearch.uk; contact@plymouthresearch.uk)`. No pretending to be Chrome. No rotating through fake browser signatures. If a site administrator looks at their access logs, they can see what visited, why, and how to contact us.

This is uncommon in scraping projects. It shouldn't be.

### Proving what we did

Every HTTP request we make is logged with a robots.txt compliance flag, the actual delay waited before the request, the HTTP status code returned, and any error message. This creates a compliance trail. If anyone questions what we accessed, when, and whether we had permission, the logs provide an auditable answer.

### Personal data and the law

We collected no personal data. Reviewer names on Trustpilot and Google are public pseudonyms, not identifiable individuals. Our legal basis under UK GDPR is legitimate interest, specifically, market research using publicly available data. We set a 12-month data retention policy and documented a Data Protection Impact Assessment before we started collecting.

### When the data disappears

One of our restaurants had a Trustpilot page when we began this project. Midway through collection, the page returned a 404. Gone. No warning, no redirect, no explanation.

This wasn't a failure. It was a lesson. Scraped data is borrowed, not owned. Platforms can remove pages, restructure their sites, or block access at any time, for any reason. This is precisely why audit logs matter. When a data source vanishes, you need to prove what you accessed and when you accessed it.

### The uncomfortable truth

Web scraping occupies a legal grey area. The UK's Computer Misuse Act and copyright law both have implications, and case law is still evolving. Open Government Licence data, from the FSA, ONS, and VOA, comes with clear, permissive terms. Web scraping does not.

We chose to treat the unclear cases with the same rigour as the clear ones. Being ethical costs nothing but attention. Implementing rate limits, honest identification, and robots.txt compliance takes hours, not weeks. The excuses for not doing it are worse than the effort of doing it.

## 6. Build This For Your City

Nothing about this project is specific to Plymouth. The methodology transfers to any city, and most of the data sources are national or global. Here is what you would need to replicate it.

### What transfers directly

FSA food hygiene data covers all of England, Wales, and Northern Ireland. To switch cities, you change a single number in the XML download URL, the local authority code. Plymouth is 891. Manchester is 352. Birmingham is 406. The data format, the rating system, and the scoring methodology are identical everywhere.

Google Places API is global. It works for restaurants in Plymouth, Paris, or Perth. Companies House covers every registered company in the United Kingdom. The ONS postcode directory maps every UK postcode to geographic coordinates, local authority boundaries, and deprivation indices.

The fuzzy matching algorithm we built is entirely location-agnostic. It scores name similarity, postcode overlap, and address word matches. It does not know or care that it is matching Plymouth restaurants. Point it at Leeds data and it works the same way.

### What needs adaptation

Menu scraping is the labour-intensive part. Every restaurant's website uses different HTML structures, different naming conventions, different levels of JavaScript rendering. You will need to build or adapt parsers for each site. There is no shortcut here. This is bespoke work.

Trustpilot coverage varies enormously by city. Plymouth's 26% coverage rate might be higher or lower elsewhere. Large cities with more chain restaurants tend to have better coverage, but independent restaurants, often the most interesting, are the hardest to find.

Council licensing data is a patchwork. Every local authority publishes differently. Some have APIs. Some have searchable websites. Some have nothing online at all. Business rates data is more standardised through the Valuation Office Agency, but presentation still varies between councils.

### What it costs

Setting up the data source fetchers took us roughly two weeks. Tuning the matching thresholds, getting the balance right between false positives and missed matches, took another two weeks. Building the Streamlit dashboard took one week. Streamlit is remarkably fast for prototyping data applications.

Total monetary cost: zero. Every data source we used is free, and Google's Places API offers a generous free tier that covers a project of this scale. The only investment is time.

### Take it further

The live dashboard is available at [dashboard link]. The full source code is available at [repository link]. We would welcome anyone adapting this approach for other cities, other sectors such as retail, healthcare, or hospitality chains, or other countries where equivalent public data exists. The data is out there. Most of it has never been combined.

## 7. What the Data Can't Tell You

We started with a simple question: why do some restaurants score perfectly on food safety and terribly on customer reviews?

The data did not answer "which restaurant should I eat at?" It answered something more interesting: what can public data tell us about a city's dining scene, and what can it not?

No single data source tells the truth. FSA ratings tell you about the kitchen on inspection day. Trustpilot tells you what motivated customers thought. Google tells you what casual visitors felt. Companies House tells you whether the business is financially viable. None of them tells the whole story. Combining them gets closer. But gaps remain, and being honest about those gaps is the point.

Every city has this data sitting in public databases, XML files, and review platforms. Most of it is never combined. The tools to do it are free. The methodology is replicable. The hardest part is not technology. It is matching "Barbican Kitchen (Original)" to "THE BARBICAN KITCHEN LTD."

*Data collected November 2025, with FSA hygiene data refreshed March 2026. All data sourced from publicly available APIs, open data, and public web pages. Food hygiene data used under the Open Government Licence v3.0. No personal data was collected or stored.*

*Explore the data yourself: [dashboard link] | View the source: [repository link]*
