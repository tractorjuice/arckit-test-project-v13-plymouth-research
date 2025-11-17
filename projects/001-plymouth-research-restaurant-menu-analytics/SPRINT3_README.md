# Sprint 3: Interactive Dashboard - README
**Date**: 2025-11-17
**Sprint**: Sprint 3 - Dashboard
**Status**: ✅ COMPLETE

## Overview

Sprint 3 delivers an interactive web dashboard for exploring Plymouth restaurant menus. Built with Streamlit, the dashboard provides powerful search, filtering, and analytics capabilities.

## Features

### 🔍 Search & Filter
- **Restaurant Selection**: Filter by one or more restaurants
- **Cuisine Type**: Filter by British Seafood, Cafe, Steakhouse, etc.
- **Price Range**: Slider to filter items by price (£0-£40+)
- **Categories**: Filter by Starters, Mains, Desserts, etc.
- **Dietary Requirements**: Filter by vegan, vegetarian, gluten-free, dairy-free

### 📊 Four Main Tabs

#### 1. Browse Menus
- View all menu items grouped by restaurant and category
- See prices, descriptions, and dietary tags
- Expandable restaurant sections
- Real-time filtering

#### 2. Price Analytics
- **Box plots** showing price distribution by category
- **Box plots** showing price distribution by restaurant
- **Histogram** of overall price distribution
- Interactive charts (zoom, pan, export)

#### 3. Restaurant Comparison
- **Menu size comparison**: Bar chart of item counts
- **Average price comparison**: Compare price points across restaurants
- **Category distribution**: Stacked bar chart showing menu composition

#### 4. Statistics
- Overall database statistics
- Restaurant details table
- Dietary tag distribution (pie chart)
- Data freshness timestamp

### 📈 Key Metrics Dashboard
- Total restaurants
- Total menu items (filtered)
- Average price (filtered)
- Number of categories

---

## Installation

### Prerequisites
- Python 3.8+
- SQLite database with restaurant data (created by `batch_scrape_restaurants.py`)

### Install Dependencies

```bash
pip install streamlit plotly pandas altair
```

Or from requirements.txt:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Run the Dashboard

```bash
streamlit run dashboard_app.py
```

The dashboard will start at **http://localhost:8501**

### 2. Open in Browser

The dashboard will automatically open in your default browser. If not, navigate to:
- **Local**: http://localhost:8501
- **Network**: http://[YOUR_IP]:8501 (for remote access)

### 3. Explore the Data

**Quick Start**:
1. Start with all filters enabled (default)
2. Browse the "Browse Menus" tab to see all restaurants
3. Use sidebar filters to narrow results:
   - Select specific restaurants
   - Set a price range (e.g., £5-£15 for casual dining)
   - Choose dietary requirements (e.g., "vegan")
4. Explore "Price Analytics" for visualizations
5. Compare restaurants in "Restaurant Comparison" tab

---

## Dashboard Walkthrough

### Sidebar Filters

```
🔍 Search & Filter
├── Restaurants (multiselect)
│   └── Default: All restaurants selected
├── Cuisine Type (multiselect)
│   └── Default: All cuisines selected
├── 💰 Price Range (slider)
│   └── Default: Min-Max from database
├── Categories (multiselect)
│   └── Default: All categories selected
└── 🥗 Dietary Requirements (multiselect)
    └── Default: None (shows all items)
```

**Note**: Dietary filter uses **AND** logic - items must have ALL selected tags.

### Example Queries

**Find vegan options under £10**:
1. Set price range: £0 - £10
2. Select dietary: "vegan"
3. Browse results in "Browse Menus" tab

**Compare steakhouse vs cafe prices**:
1. Select restaurants: "The Plymouth Grill", "The Boathouse Cafe"
2. Go to "Price Analytics" tab
3. See price distribution box plots

**Find all starters**:
1. Select categories: "Starters"
2. Browse all restaurants' starter menus

---

## Data Sources

The dashboard connects to `plymouth_research.db` (SQLite database) with the following tables:
- `restaurants` - Restaurant metadata (3 restaurants)
- `menu_items` - Menu item details (54 items)
- `dietary_tags` - Reference data (5 tags)
- `menu_item_dietary_tags` - Junction table for item-tag relationships

### Data Refresh

Data is cached for **5 minutes** (TTL=300s) for performance. To refresh:
- Restart the dashboard
- Or wait 5 minutes for automatic cache expiration

To re-scrape restaurants and update the database:

```bash
python batch_scrape_restaurants.py
```

---

## Technical Details

### Architecture

```
dashboard_app.py
├── Streamlit UI Framework
├── SQLite Database Connection (cached)
├── Pandas DataFrames (cached queries)
├── Plotly Charts (interactive)
└── Filter Logic (real-time)
```

### Performance Optimizations

1. **Database Connection Caching**: `@st.cache_resource`
   - Single connection reused across requests
   - Prevents connection overhead

2. **Data Query Caching**: `@st.cache_data(ttl=300)`
   - Queries cached for 5 minutes
   - Reduces database load

3. **Client-Side Filtering**: All filters applied in-memory (fast)

### Chart Libraries

- **Plotly Express**: Box plots, bar charts, histograms
- **Plotly Graph Objects**: Advanced customization
- **Altair**: Alternative visualization library (not currently used)

---

## Troubleshooting

### Dashboard Won't Start

**Error**: `Database not found: plymouth_research.db`

**Solution**: Run the batch scraper first:
```bash
python batch_scrape_restaurants.py
```

### Empty Dashboard

**Error**: No data showing despite database existing

**Solution**: Check database has data:
```bash
sqlite3 plymouth_research.db "SELECT COUNT(*) FROM menu_items;"
```

Expected output: `54` (or more)

### Port Already in Use

**Error**: `Address already in use`

**Solution**: Stop existing Streamlit process or use different port:
```bash
streamlit run dashboard_app.py --server.port 8502
```

### Filters Not Working

**Issue**: Dietary filter returns no results

**Cause**: Using AND logic - items must have ALL selected tags

**Solution**: Select fewer dietary tags or check data coverage

---

## Deployment

### Local Development
```bash
streamlit run dashboard_app.py
```

### Production Deployment

#### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect repository at https://streamlit.io/cloud
3. Deploy with one click
4. Free tier available

#### Option 2: Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t plymouth-dashboard .
docker run -p 8501:8501 plymouth-dashboard
```

#### Option 3: Cloud VM (AWS, GCP, Azure)
1. Provision VM with Python 3.8+
2. Install dependencies
3. Run with systemd service:

```ini
# /etc/systemd/system/plymouth-dashboard.service
[Unit]
Description=Plymouth Restaurant Dashboard
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/plymouth-research
ExecStart=/usr/bin/streamlit run dashboard_app.py --server.port=8501 --server.headless=true
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable plymouth-dashboard
sudo systemctl start plymouth-dashboard
```

---

## Sprint 3 Deliverables

### User Stories Completed

- ✅ **US-011**: Search by cuisine/price/dietary (8 SP)
- ✅ **US-012**: Price comparison charts (8 SP)
- ✅ **US-013**: Filter by dietary requirements (5 SP)
- ✅ **US-014**: Streamlit/Dash UI (13 SP)

**Total**: 34 Story Points delivered

### Files Created

- `dashboard_app.py` (450 lines) - Main Streamlit application
- `SPRINT3_README.md` - This documentation
- Updated `requirements.txt` - Added Streamlit, Plotly, Pandas, Altair

### Features Implemented

1. **Search & Filtering**: 6 filter types (restaurant, cuisine, price, category, dietary)
2. **4 Dashboard Tabs**: Browse, Analytics, Comparison, Statistics
3. **8 Interactive Charts**: Box plots, bar charts, histograms, pie charts
4. **4 Key Metrics**: Real-time statistics at top of page
5. **Data Caching**: 5-minute cache for performance
6. **Responsive Design**: Wide layout with collapsible sidebar

---

## Next Steps (Sprint 4+)

### Sprint 4: Dashboard Enhancements (11 SP)
- ✅ Deployment to Streamlit Cloud/AWS
- User authentication
- Export functionality (CSV, PDF)
- Favorite restaurants
- Menu comparison view

### Sprint 5: API Development (20 SP)
- REST API with FastAPI
- Endpoints: `/restaurants`, `/menu-items`, `/search`
- API documentation (Swagger)
- Rate limiting

### Sprint 6: Automation (20 SP)
- Scheduled weekly scraping (cron)
- Email notifications on new menus
- Data quality monitoring
- Automated testing

---

## Screenshots

### Main Dashboard
![Dashboard Overview](https://via.placeholder.com/800x400?text=Dashboard+Overview)

### Price Analytics
![Price Analytics](https://via.placeholder.com/800x400?text=Price+Analytics)

### Restaurant Comparison
![Restaurant Comparison](https://via.placeholder.com/800x400?text=Restaurant+Comparison)

---

## Support

**Issues**: Report issues to the Plymouth Research Architecture Team

**Documentation**: See `README.md` in project root

**Database Schema**: See `database/schema_sqlite.sql`

---

## License

Internal project - Plymouth Research Team
Confidential - Not for public distribution

---

**Last Updated**: 2025-11-17
**Version**: 1.0
**Status**: Production Ready ✅
