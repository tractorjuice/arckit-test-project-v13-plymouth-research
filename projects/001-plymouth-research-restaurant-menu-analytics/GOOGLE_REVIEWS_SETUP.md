# Google Reviews Integration - Setup Guide

**Status**: Ready for API Key Setup
**Date**: 2025-11-19
**Author**: Claude Code

---

## Quick Start

### Step 1: Get Google Cloud API Key

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create or select a project**:
   - Click "Select a project" → "New Project"
   - Name: "Plymouth Restaurant Research"
   - Click "Create"

3. **Enable Places API (New)**:
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search for "Places API (New)"
   - Click "Enable"

4. **Create API Key**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key (looks like: `AIzaSyD...`)

5. **Restrict API Key** (Security Best Practice):
   - Click on the newly created key
   - Under "API restrictions":
     - Select "Restrict key"
     - Choose "Places API (New)"
   - Click "Save"

### Step 2: Set Environment Variable

**Option A: Temporary (current session only)**
```bash
export GOOGLE_PLACES_API_KEY="AIzaSyD_your_actual_key_here"
```

**Option B: Permanent (.bashrc or .zshrc)**
```bash
echo 'export GOOGLE_PLACES_API_KEY="AIzaSyD_your_actual_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Option C: .env File** (Recommended for projects)
```bash
# Create .env file in project directory
echo "GOOGLE_PLACES_API_KEY=AIzaSyD_your_actual_key_here" > .env

# Install python-dotenv (if not already installed)
pip install python-dotenv
```

### Step 3: Verify Setup

```bash
# Check if API key is set
echo $GOOGLE_PLACES_API_KEY

# Test with a single restaurant
python fetch_google_reviews.py --restaurant-id 4
```

---

## API Costs & Limits

### Free Tier
- **$200 credit per month** (renewable every month)
- ~11,700 requests/month free
- New accounts get additional $300 credit for 90 days

### Pricing (after free credit)
- **Find Place (Text Search)**: $17 per 1,000 requests
- **Place Details**: $17 per 1,000 requests

### Cost Estimate for This Project
- **98 restaurants** = 196 requests (search + details)
- **One-time cost**: ~$3.40
- **Monthly updates**: ~$3.40/month if refreshing all restaurants

**Conclusion**: Free tier is more than sufficient for this project!

---

## Usage Examples

### Test Mode (5 restaurants)
```bash
python fetch_google_reviews.py --test
```
Expected output:
- 5 restaurants processed
- ~5 reviews per restaurant (25 total)
- ~10 API requests (~$0.17)

### Single Restaurant
```bash
python fetch_google_reviews.py --restaurant-id 4
```
This is the safest way to test initially.

### All Restaurants
```bash
python fetch_google_reviews.py --all
```
Expected output:
- 98 restaurants processed
- ~490 reviews total (5 per restaurant, API limit)
- 196 API requests (~$3.40)

### Incremental Update (Only New)
```bash
python fetch_google_reviews.py --update
```
Only fetches restaurants without `google_place_id` (not yet processed).

---

## What Google Reviews Provides

### Advantages
- ✅ **Universal Coverage**: 95%+ of restaurants have Google Business profiles
- ✅ **Official API**: Stable, reliable, legal
- ✅ **Location-Specific**: Reviews tied to specific restaurant location
- ✅ **Rich Metadata**: Author photos, relative time, language
- ✅ **Google Rating**: Visible rating (1-5 stars) from Google Maps

### Limitations
- ⚠️ **5 Reviews Max**: API only returns 5 most recent reviews per location
- ⚠️ **No Review History**: Cannot fetch older reviews beyond the 5 most recent
- ⚠️ **API Cost**: Minimal cost after free tier ($3.40 for 98 restaurants)

### Complement with Trustpilot
- **Google**: 5 reviews × 98 restaurants = ~490 reviews (high coverage, recent only)
- **Trustpilot**: 9,410 reviews from 63 restaurants (deep history, limited coverage)
- **Combined**: Best of both worlds!

---

## Database Schema

### New Columns in `restaurants` Table
```sql
google_place_id              TEXT     -- Google's unique place identifier
google_rating                REAL     -- Overall Google rating (1-5)
google_user_ratings_total    INTEGER  -- Total number of ratings on Google
google_price_level           INTEGER  -- Price level (0-4: Free to Very Expensive)
google_last_fetched_at       TEXT     -- Last fetch timestamp
google_review_count          INTEGER  -- Count of reviews in our DB (max 5)
google_avg_rating            REAL     -- Average of our stored reviews
```

### New `google_reviews` Table
```sql
CREATE TABLE google_reviews (
    review_id                   INTEGER PRIMARY KEY,
    restaurant_id               INTEGER,
    review_date                 TEXT,
    author_name                 TEXT,
    review_text                 TEXT,
    rating                      INTEGER (1-5),
    google_author_url           TEXT,
    google_profile_photo_url    TEXT,
    language                    TEXT,
    relative_time_description   TEXT,
    fetched_at                  TEXT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);
```

---

## Troubleshooting

### Error: "API key not set"
```bash
# Check if environment variable is set
echo $GOOGLE_PLACES_API_KEY

# If empty, set it
export GOOGLE_PLACES_API_KEY="your-key-here"
```

### Error: "API key not valid"
- Check key is copied correctly (no extra spaces)
- Verify Places API (New) is enabled in Google Cloud Console
- Check API key restrictions (should allow Places API)

### Error: "Quota exceeded"
- You've used up free tier credits
- Check usage in Google Cloud Console → "APIs & Services" → "Dashboard"
- Either wait for monthly reset or add billing

### Error: "Place not found"
- Restaurant may not have a Google Business profile
- Try manual search on Google Maps to confirm
- Check restaurant name/address spelling

### No Reviews Returned
- This is normal - some places have no reviews
- Google may have reviews but API doesn't return them (privacy filters)
- API only returns max 5 reviews (limitation)

---

## Next Steps

1. **Get API Key** (see Step 1 above)
2. **Set Environment Variable** (see Step 2)
3. **Test with Single Restaurant**:
   ```bash
   python fetch_google_reviews.py --restaurant-id 4
   ```
4. **Run Full Fetch**:
   ```bash
   python fetch_google_reviews.py --all
   ```
5. **Update Dashboard** to show Google Reviews (next phase)

---

## Comparison: Google vs Trustpilot

| Feature | Google Places API | Trustpilot Scraping |
|---------|------------------|---------------------|
| **Coverage** | 95%+ (98 restaurants) | 64% (63 restaurants) |
| **Reviews per Restaurant** | 5 (API limit) | 50-200 (full history) |
| **Total Reviews Expected** | ~490 | 9,410 ✓ |
| **Historical Data** | Recent only (5) | 12 years ✓ |
| **Location Specific** | Yes ✓ | Sometimes (chains are company-wide) |
| **Official API** | Yes ✓ | No (scraping) |
| **Cost** | $3.40 one-time | Free |
| **Legal/Ethical** | 100% compliant ✓ | Grey area (ToS) |
| **Data Freshness** | Real-time | Manual refresh |
| **Best For** | Recent sentiment, high coverage | Historical trends, deep analysis |

**Recommendation**: Use both! They complement each other perfectly.

---

*Last Updated: 2025-11-19*
*Status: Ready for API key setup*
