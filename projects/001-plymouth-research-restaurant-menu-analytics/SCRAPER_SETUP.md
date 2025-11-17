# Automated Scraper Setup Guide

## Overview

The automated scraper periodically checks restaurant websites for menu updates and refreshes the database with the latest information.

## Features

- **Robots.txt Compliance**: Checks and respects robots.txt before scraping
- **Rate Limiting**: Enforces 5-second delays between requests per domain
- **Error Handling**: Logs all attempts and handles failures gracefully
- **Change Detection**: Only updates database when menu changes are detected
- **Comprehensive Logging**: All activities logged to `scraper.log`

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

(Already included in requirements.txt)

### 2. Test Manual Run

```bash
# From project root directory
python src/scrapers/automated_scraper.py
```

You should see output showing scraping attempts for all 11 restaurants.

### 3. Schedule with Cron (Linux/Mac)

Make the cron script executable:

```bash
chmod +x cron_scraper.sh
```

Edit your crontab:

```bash
crontab -e
```

Add one of these lines based on your preferred schedule:

```bash
# Every Sunday at 2am
0 2 * * 0 /path/to/cron_scraper.sh

# Every day at 3am
0 3 * * * /path/to/cron_scraper.sh

# Every Monday at 1am
0 1 * * 1 /path/to/cron_scraper.sh

# Twice per week (Wednesday and Sunday at 2am)
0 2 * * 0,3 /path/to/cron_scraper.sh
```

### 4. Schedule with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Weekly on Sunday at 2am)
4. Set action: Start a program
5. Program: `python`
6. Arguments: `src/scrapers/automated_scraper.py`
7. Start in: `<project_directory>`

## Architecture

### Core Components

```
src/scrapers/
├── __init__.py
└── automated_scraper.py       # Main scraper class

src/database/
└── connection.py               # Database with scraping logs

cron_scraper.sh                 # Cron job wrapper script
scraper.log                     # Scraper activity log (auto-created)
scraper_cron.log                # Cron job log (auto-created)
```

### RestaurantScraper Class

**Methods:**
- `check_robots_txt(url)` - Verify scraping is allowed
- `rate_limit(url)` - Enforce 5-second delay between requests
- `scrape_restaurant(restaurant)` - Scrape single restaurant
- `update_restaurant_menu(restaurant, items)` - Update if changed
- `scrape_all()` - Scrape all restaurants in database

### Database Integration

All scraping attempts are logged in the `scraping_logs` table:

```sql
CREATE TABLE scraping_logs (
    log_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER,
    url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    http_status_code INTEGER,
    robots_txt_allowed BOOLEAN,
    rate_limit_delay_seconds INTEGER,
    user_agent TEXT,
    success BOOLEAN,
    error_message TEXT
);
```

## Configuration

### Rate Limiting

Default: 5 seconds between requests per domain

To change, edit `automated_scraper.py`:

```python
self.rate_limit_seconds = 10  # 10 seconds
```

### User Agent

Default: `PlymouthResearchBot/1.0 (Educational Research; respectful scraper)`

To change, edit `automated_scraper.py`:

```python
self.user_agent = "YourBot/1.0 (contact@example.com)"
```

## Monitoring

### Check Scraper Logs

```bash
# View recent scraping activity
tail -f scraper.log

# View cron job execution
tail -f scraper_cron.log
```

### Query Scraping History

```sql
-- Recent scraping attempts
SELECT
    r.name,
    sl.scraped_at,
    sl.success,
    sl.error_message
FROM scraping_logs sl
JOIN restaurants r ON sl.restaurant_id = r.restaurant_id
ORDER BY sl.scraped_at DESC
LIMIT 20;

-- Success rate by restaurant
SELECT
    r.name,
    COUNT(*) as total_attempts,
    SUM(CASE WHEN sl.success THEN 1 ELSE 0 END) as successful,
    ROUND(100.0 * SUM(CASE WHEN sl.success THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM scraping_logs sl
JOIN restaurants r ON sl.restaurant_id = r.restaurant_id
GROUP BY r.name
ORDER BY success_rate DESC;
```

## Current Limitations

### Parser Not Implemented

The current scraper has a **placeholder parser** (`_parse_menu` method). To fully automate scraping, you need to implement restaurant-specific parsers.

**Example implementation:**

```python
def _parse_menu(self, html: str, restaurant_name: str) -> Optional[List[Dict]]:
    """Parse menu items from HTML."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')

    # Example: Parse The Village Restaurant
    if restaurant_name == "The Village Restaurant":
        menu_items = []

        # Find menu sections
        for item in soup.find_all('div', class_='menu-item'):
            name = item.find('h3', class_='item-name').text.strip()
            desc = item.find('p', class_='item-desc').text.strip()
            price = item.find('span', class_='price').text.strip()

            # Parse price (remove £ symbol)
            price_gbp = float(price.replace('£', ''))

            menu_items.append({
                'name': name,
                'description': desc,
                'price_gbp': price_gbp,
                'category': 'Unknown',  # Determine from section
                'dietary_tags': []
            })

        return menu_items

    return None
```

### Recommended Approach

For production use, consider:

1. **BeautifulSoup** for HTML parsing
2. **Scrapy** for complex multi-page scraping
3. **Selenium** for JavaScript-heavy sites
4. **API integrations** where available (e.g., Deliveroo API)
5. **LLM-based parsing** for unstructured menus (using Claude or GPT)

## Ethical Considerations

### Respect Website Resources

- **Rate limiting**: 5 seconds minimum between requests
- **robots.txt**: Always check and respect
- **Off-peak hours**: Schedule scraping during low-traffic times
- **User agent**: Clearly identify as a bot with contact info

### Legal Compliance

- **Copyright**: Transformative use for analytics, not republication
- **Terms of Service**: Review each restaurant's website TOS
- **GDPR**: Only collect public business data, no personal information
- **Attribution**: Link back to original sources in dashboard

## Troubleshooting

### Scraper Not Running

Check cron is active:
```bash
sudo service cron status
```

Check crontab syntax:
```bash
crontab -l
```

### No Logs Generated

Ensure write permissions:
```bash
chmod 755 /path/to/project
touch scraper.log scraper_cron.log
```

### HTTP 403 Errors

Website may be blocking automated access:
- Check robots.txt
- Verify user agent is acceptable
- Consider API integration instead

### Parser Returns No Items

Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

Check HTML structure matches parser expectations.

## Future Enhancements

1. **WebFetch Integration**: Use Claude's WebFetch for AI-powered extraction
2. **Diff Detection**: More sophisticated change detection (not just count)
3. **Notifications**: Email/Slack alerts on failures
4. **Dashboard Integration**: "Refresh Now" button in dashboard
5. **Multi-threading**: Parallel scraping with asyncio
6. **Menu Versioning**: Track historical menu changes
7. **Price Trend Analysis**: Alert on significant price changes

## Support

For issues or questions:
- Check `scraper.log` for error details
- Review scraping_logs table in database
- Consult BeautifulSoup/Scrapy documentation
- Contact: Plymouth Research Team

---

**Last Updated**: 2025-11-17
**Version**: 1.0
