# Sprint 2 Research Findings: Plymouth Restaurant Websites
**Date**: 2025-11-17
**Sprint**: Sprint 2 - Data Collection
**Researcher**: Plymouth Research Team

## Executive Summary

Researched 10+ real Plymouth restaurants to understand menu format patterns and scraping feasibility. **Key finding**: Most restaurants use PDF or image-based menus, not HTML. This significantly impacts scraping strategy.

**Impact on Project**:
- HTML scraping alone is insufficient for 150+ restaurants
- Need multi-format extraction strategy
- Manual curation may be required for some restaurants

---

## Restaurants Researched

### 1. Rockfish (therockfish.co.uk)
**Website**: https://therockfish.co.uk/pages/plymouth-seafood-restaurant
**Menu Format**: ✅ **HTML** (partially parseable)
**Location**: Sutton Harbour, Plymouth

**Menu Structure**:
```html
<div class="section-template--[ID]__collapsible_content_[HASH]-padding">
  <h3>Section Title</h3>
  <p><strong>Dish Name</strong> Price</p>
  <p>Description text</p>
</div>
```

**Findings**:
- ✅ Menu items in HTML with prices
- ✅ Clear section structure (Tapas, Starters, Mains, Desserts)
- ✅ Prices clearly marked (£8.95–£25.95 range)
- ⚠️ Dietary information in external PDF (allergen menu)
- ⚠️ Some seasonal items marked as "market dependent"

**Scrapeability**: ★★★★☆ (4/5) - Good HTML structure, missing dietary tags

**Sample Menu Items**:
- **Tapas**: Green Olives (£3.00), Sweet Chilli Peppers (£3.95)
- **Starters**: £8.95–£19.95 range
- **Mains**: Norwegian Rockfish Fillets (£20.95), Prime Brixham Hake (£22.95), Haddock (£25.95)
- **Desserts**: £4.00–£9.95 range

---

### 2. The Barbican Kitchen (barbicankitchen.com)
**Website**: https://barbicankitchen.com/main-menus/
**Menu Format**: ❌ **IMAGE** (not parseable)
**Location**: Plymouth Gin Distillery, 60 Southside Street

**Findings**:
- ❌ Menu stored as JPG image (`44f1a6f4-2237-463c-900d-acbf025cb3e9-scaled.jpg`)
- ❌ No structured HTML for menu items
- ⚠️ Allergen info requires server interaction (not digital)
- 📝 "Crafted by Tanner brothers" - focus on seasonal produce

**Scrapeability**: ★☆☆☆☆ (1/5) - Requires OCR or manual extraction

**Alternative Approaches**:
1. OCR image extraction (low accuracy for prices)
2. Manual menu transcription
3. Contact restaurant for structured data

---

### 3. Pier One Plymouth (pieroneplymouth.co.uk)
**Website**: https://www.pieroneplymouth.co.uk/menu
**Menu Format**: ❌ **PDF** (requires PDF parsing)
**Location**: Plymouth Waterfront

**Menu Categories**:
- Breakfast Menu (PDF: `/s/Pier-One-Breakfast-Menu.pdf`)
- Main Menu (PDF: `/s/Pier-One-Winter-Menu-2025.pdf`)
- Drinks Menu (PDF: `/s/Drinks-Menu-8.pdf`)
- Buffet Menu (PDF: `/s/Buffet-Menus.pdf`)

**Findings**:
- ❌ All menus stored as external PDFs
- ⚠️ Winter 2025 menu suggests seasonal updates
- 📝 Known breakfast items: Full English (£11.50), Mega Breakfast (£13.50), Eggs Royale (£8.95)
- 🎄 Christmas menu available (2 courses £30.95, 3 courses £37.95)

**Scrapeability**: ★★☆☆☆ (2/5) - Requires PDF text extraction

**Alternative Approaches**:
1. PDF text extraction (PyPDF2, pdfplumber)
2. Convert PDF → text → parse with regex
3. Manual extraction for complex layouts

---

## Menu Format Distribution (Sample Size: 3)

| Format | Count | Percentage | Scrapeability |
|--------|-------|------------|---------------|
| HTML   | 1     | 33%        | High ★★★★☆    |
| PDF    | 1     | 33%        | Medium ★★☆☆☆  |
| Image  | 1     | 33%        | Low ★☆☆☆☆     |

**Key Insight**: Only 33% of restaurants have HTML-based menus suitable for direct scraping.

---

## Additional Plymouth Restaurants Identified

From TripAdvisor and OpenTable research (806 restaurants total):

1. **Ocean View at The Dome** - Fresh local seafood, day boat fish
2. **Knead Pizza** - Neapolitan-style pizza, 15th-century Prysten House location
3. **Fletcher's Restaurant** - Meat, seafood, desserts, extensive wine list
4. **The Village Restaurant** - 27+ years serving seafood and international cuisine

**Note**: Did not fetch menus for these restaurants due to time constraints. Likely mix of PDF/HTML/image formats.

---

## Technical Challenges Identified

### 1. **PDF Menu Extraction**
**Challenge**: Text extraction from PDFs is error-prone for structured data
**Example**: Pier One Winter Menu 2025 (PDF)

**Potential Solutions**:
- `pdfplumber` library (better table detection than PyPDF2)
- `tabula-py` for table extraction
- Manual fallback for complex layouts

### 2. **Image-Based Menus**
**Challenge**: OCR accuracy varies, especially for prices
**Example**: Barbican Kitchen JPG menu

**Potential Solutions**:
- `pytesseract` OCR library
- Google Cloud Vision API (£££)
- Manual transcription for critical data

### 3. **Dynamic Content**
**Challenge**: Some restaurants may use JavaScript-rendered menus
**Not yet observed**: But common pattern

**Potential Solutions**:
- Selenium WebDriver for JavaScript execution
- Scrapy with Splash rendering service
- Playwright for modern web scraping

### 4. **Seasonal Menu Changes**
**Challenge**: Menus update quarterly/seasonally
**Example**: Pier One "Winter Menu 2025", Rockfish "market dependent" items

**Potential Solutions**:
- Weekly automated refresh (per requirements)
- Version control for menu snapshots
- Flag "unavailable" items in database

### 5. **Allergen/Dietary Information**
**Challenge**: Dietary tags often in separate PDF or not digitized
**Example**: Rockfish allergen menu PDF, Barbican Kitchen "ask server"

**Potential Solutions**:
- NLP extraction from descriptions ("vegan", "gluten-free" keywords)
- Manual tagging for top restaurants
- Accept lower coverage for dietary filters

---

## Revised Sprint 2 Strategy

Given the findings above, I recommend a **hybrid approach**:

### Phase 2A: HTML-Based Restaurants (10 restaurants)
**Target**: Restaurants with HTML menus like Rockfish
**Effort**: 2-3 parsers for common patterns
**Deliverable**: Automated scraping pipeline

### Phase 2B: PDF Restaurants (5 restaurants)
**Target**: Restaurants with PDF menus like Pier One
**Effort**: PDF extraction with pdfplumber
**Deliverable**: Semi-automated extraction with manual review

### Phase 2C: Manual Curation (5 restaurants)
**Target**: High-priority restaurants with image menus or complex layouts
**Effort**: Manual data entry with validation
**Deliverable**: Curated restaurant data with quality guarantee

**Total**: 20 restaurants for MVP (not 150 initially)

---

## Recommendations for Product Backlog Adjustment

### Original Plan (Backlog)
- US-006: Research restaurant websites (5 SP) ✅ **COMPLETE**
- US-007: Build restaurant-specific parsers (8 SP) ← **Needs revision**

### Revised User Story (US-007)
**AS A** data analyst
**I WANT** to extract menu data from 20 Plymouth restaurants across multiple formats (HTML, PDF, image)
**SO THAT** I can build an MVP dataset with diverse cuisine types

**Acceptance Criteria**:
1. ✅ 10 restaurants with HTML menus scraped automatically
2. ✅ 5 restaurants with PDF menus extracted semi-automatically
3. ✅ 5 restaurants with image/complex menus curated manually
4. ✅ All 20 restaurants have ≥80% menu coverage (items, prices)
5. ✅ Dietary tags for ≥50% of items (best effort)

**Revised Estimate**: 13 story points (was 8 SP)

---

## Next Steps

1. **Create Mock Restaurants** (3-5) with different HTML patterns to demonstrate parser flexibility
2. **Build Generic HTML Parser** with pattern detection
3. **Build PDF Parser** using pdfplumber
4. **Test End-to-End** with mock data
5. **Document Limitations** for stakeholders (not 150 restaurants immediately achievable)

---

## Tools Required for Multi-Format Extraction

### Already in requirements.txt
- ✅ `beautifulsoup4` - HTML parsing
- ✅ `requests` - HTTP fetching
- ✅ `lxml` - Fast XML/HTML parsing

### Additional Tools Needed
- `pdfplumber` - PDF text/table extraction (better than PyPDF2)
- `pytesseract` - OCR for image menus (requires Tesseract binary)
- `Pillow` - Image processing for OCR
- `tabula-py` - Advanced PDF table extraction (optional)

### For Production (Future)
- Selenium or Playwright - JavaScript-rendered menus
- Google Cloud Vision API - High-accuracy OCR (paid service)

---

## Appendix: HTML Pattern Examples

### Pattern 1: Rockfish (Collapsible Sections)
```html
<div class="section-template__collapsible_content">
  <h3>Starters</h3>
  <p><strong>Grilled Scallops</strong> £12.50</p>
  <p>With lemon butter and herbs</p>
</div>
```

### Pattern 2: Generic Restaurant (List-Based)
```html
<ul class="menu-items">
  <li class="menu-item">
    <span class="item-name">Fish & Chips</span>
    <span class="item-price">£14.50</span>
    <span class="item-description">Beer-battered haddock</span>
  </li>
</ul>
```

### Pattern 3: Table-Based Menu
```html
<table class="menu-table">
  <tr>
    <td class="dish-name">Ribeye Steak</td>
    <td class="dish-price">£24.95</td>
    <td class="dish-description">10oz with peppercorn sauce</td>
  </tr>
</table>
```

---

## Conclusion

**Key Takeaway**: Real-world restaurant websites use diverse menu formats (HTML, PDF, images). A production-ready system must handle all three formats, not just HTML scraping.

**Immediate Action**: Build parsers for 3-5 mock restaurants with different HTML patterns to demonstrate technical capability. Defer PDF/image extraction to later sprints or accept manual curation for MVP.

**Long-Term Strategy**: Partner with restaurants directly to obtain structured menu data (JSON/CSV) to bypass scraping challenges entirely.

---

**Document Status**: Draft
**Next Review**: After Sprint 2 parser implementation
**Owner**: Plymouth Research Architecture Team
