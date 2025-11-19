# Companies House Integration Guide

This guide explains how to fetch and integrate Companies House business data for your restaurants.

## What You'll Get

Adding Companies House data provides valuable business intelligence:

- **Company Registration**: Legal company name and number
- **Business Status**: Active, dissolved, in administration, etc.
- **Incorporation Date**: How long the business has been operating
- **Company Type**: Limited, PLC, LLP, sole trader, etc.
- **Directors**: Company officers and management
- **Registered Address**: Official company address
- **SIC Codes**: Business activity classification
- **Financial Data**: Latest accounts filing date, turnover (if available)

## Step 1: Get Your API Key (5 minutes)

Companies House provides a **free API** with generous rate limits.

1. Go to: https://developer.company-information.service.gov.uk/
2. Click **"Register"** (top right)
3. Fill in your details and verify your email
4. Log in and click **"Your applications"**
5. Click **"Create an application"**
6. Fill in:
   - **Application name**: "Plymouth Restaurant Research"
   - **Description**: "Restaurant market research and analytics"
   - **Environment**: "Live"
7. Click **"Create"**
8. Your **API key** will be displayed - copy it (it looks like: `a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6`)

**Important**: Keep your API key secret - don't commit it to git!

## Step 2: Run the Discovery Script

The script will search Companies House for each of your 243 restaurants and export matches to CSV files for review.

### Option A: Set Environment Variable (Recommended)

```bash
export COMPANIES_HOUSE_API_KEY="your-api-key-here"
python fetch_companies_house_data.py
```

### Option B: Enter When Prompted

```bash
python fetch_companies_house_data.py
# When prompted, paste your API key
```

### What Happens

The script will:
1. Connect to Companies House API
2. Search for each restaurant by name
3. Score matches based on:
   - Name similarity
   - Postcode match
   - Plymouth area check
   - Company status
   - SIC codes (restaurant classification)
4. Export results to 4 CSV files based on confidence

**Time**: ~10-15 minutes for 243 restaurants (respects API rate limits)

## Step 3: Review the Results

The script generates 4 CSV files:

### 1. `companies_high_confidence.csv` (≥70% confidence)

**What to do**: ✅ **Safe to import directly**

These are very likely correct matches:
- Exact or near-exact name match
- Postcode matches
- Company is active
- Restaurant SIC codes

**Example**:
```
Restaurant: "Rockfish Plymouth"
Company: "Rockfish Restaurants Limited"
Confidence: 95.5% (exact_name, postcode_match, plymouth_area, active, restaurant_sic)
```

### 2. `companies_medium_confidence.csv` (50-69% confidence)

**What to do**: ⚠️ **Manual verification recommended**

These might be correct but need a quick review:
- Similar names (e.g., "Barbican Kitchen" → "Barbican Kitchen Brasserie")
- Postcode nearby but not exact
- Trading name vs legal name differences

**How to verify**:
1. Check registered address matches
2. Look up company on Companies House website
3. Verify directors if you know the owner
4. Check incorporation date makes sense

### 3. `companies_low_confidence.csv` (30-49% confidence)

**What to do**: ⚠️ **Likely incorrect - review carefully**

These are probably wrong matches:
- Name similarity is low
- Different area of Plymouth
- Wrong type of business

**Decision**: Most should be rejected, but check a few manually

### 4. `companies_no_match.csv` (<30% confidence)

**What to do**: ℹ️ **Probably sole traders or trading names**

These restaurants likely:
- Are sole traders (not limited companies)
- Use a trading name that's very different from legal name
- Are franchises (owned by individual franchisee companies)
- Are new businesses not yet registered

**Note**: Not being a limited company is perfectly normal for restaurants!

## Step 4: Manual Verification (Optional but Recommended)

For medium confidence matches, verify on Companies House website:

1. Go to: https://find-and-update.company-information.service.gov.uk/
2. Search for the company number from the CSV
3. Check:
   - ✅ Registered address is in Plymouth
   - ✅ Directors make sense (if you know the owners)
   - ✅ Company type is appropriate (Ltd, PLC, LLP)
   - ✅ Status is "Active"
   - ✅ SIC codes include restaurants (56101, 56102, 56103)

If it looks wrong:
- Move it to the "reject" pile
- Try searching manually with different terms
- The restaurant might be a trading name

## Step 5: Import to Database (Coming Next)

Once you're happy with the high confidence matches, you can import them to the database.

I'll create an import script that:
1. Reads `companies_high_confidence.csv`
2. Creates a `companies` table in the database
3. Links companies to restaurants
4. Optionally fetches director information
5. Updates the dashboard to show company info

**Manual import option** (if you edited the CSV):
```bash
python import_companies_house_data.py --file companies_high_confidence.csv
```

## Expected Results

Based on typical restaurant populations:

- **High Confidence**: ~40-50% (100-120 restaurants)
  - These are established limited companies with clear names

- **Medium Confidence**: ~10-15% (25-35 restaurants)
  - Trading names, similar names, need quick check

- **Low/No Match**: ~35-50% (85-120 restaurants)
  - Sole traders, franchises, new businesses, trading names

**Important**: Not finding a company match doesn't mean the restaurant is illegitimate - many successful restaurants are sole traders!

## Troubleshooting

### "API key is invalid"
- Check you copied the entire key (36 characters with hyphens)
- Make sure it's from the "Live" environment, not "Sandbox"
- Verify your application is "Registered" status

### "Too many requests"
- The script automatically rate limits (600 per 5 minutes)
- If you run it multiple times quickly, wait 5 minutes

### "No results for obvious companies"
- Try searching manually on Companies House website
- The company might be registered under a parent company name
- Check for spelling variations (e.g., "&" vs "and")

### "Wrong company matched"
- This is why we have confidence scores!
- Reject it and try manual search
- Add notes in the CSV before importing

## Data Quality Tips

### Common Scenarios

**Chains & Franchises**:
- National chains: Parent company (e.g., "Pizza Express Restaurants Limited")
- Franchises: Individual franchisee company (e.g., "Smith Plymouth Pizza Ltd")

**Trading Names**:
- Legal: "Plymouth Hospitality Group Ltd"
- Trading as: "The Waterfront Restaurant"
- Solution: Check "Previous company names" on Companies House

**Multiple Locations**:
- One company, multiple restaurants
- Solution: Note in database, link all locations to same company

**Dissolved Companies**:
- Restaurant may have new owners
- New company number
- Check incorporation date vs restaurant opening

## Privacy & Legal

✅ **Legal to use**:
- Companies House data is public and open
- Free to access, use, and redistribute
- No restrictions on commercial or non-commercial use

✅ **Attribution**:
- Recommended: "Company information from Companies House"
- Not legally required but good practice

✅ **Data Protection**:
- Company data is public business information
- Director names are public (not PII in this context)
- Financial data is aggregate (turnover/profit, not detailed)

## Next Steps

After importing company data:

1. **Dashboard Integration**: Show company info in Restaurant Profiles tab
2. **Business Intelligence Tab**: Create analysis of company types, ages, financial health
3. **Director Information**: Optionally fetch and display directors
4. **Financial Data**: Add latest accounts information
5. **Monitoring**: Set up quarterly refresh to check for status changes

## API Limits & Costs

- **Rate Limit**: 600 requests per 5 minutes
- **Cost**: £0 (completely free)
- **Daily Usage**: No limit
- **Monthly Usage**: No limit

For 243 restaurants:
- Initial discovery: ~500-1000 requests (~10-15 minutes)
- Monthly refresh: ~250 requests (~5 minutes)
- Director fetch: ~150 requests (~3 minutes)

**Total time**: ~20-25 minutes for full data collection

## Support

If you have questions:
1. Check Companies House API docs: https://developer.company-information.service.gov.uk/api/docs/
2. Review the script: `fetch_companies_house_data.py`
3. Test with a single restaurant first before running full batch

---

**Created**: 2025-11-19
**Version**: 1.0
**Script**: `fetch_companies_house_data.py`
