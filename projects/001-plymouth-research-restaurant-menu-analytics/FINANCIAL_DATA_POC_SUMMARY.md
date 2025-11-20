# Financial Data POC Summary - Honky Tonk Wine Library

**Date**: 2025-11-20
**Company**: HONKYTONK WINE LIBRARY LIMITED (11403510)
**POC Scripts**: `poc_financial_data.py`, `poc_download_accounts.py`, `poc_parse_ixbrl.py`

---

## Executive Summary

✅ **Phase 1 (Filing Metadata)** is viable and recommended
⚠️ **Phase 2 (Financial Metrics)** has limited value due to micro-entity exemptions

---

## What We Found for Honky Tonks

### Company Profile (from API)
- **Status**: Active
- **Incorporated**: 2018-06-07 (7 years old)
- **Type**: Private Limited Company (ltd)
- **SIC Codes**: 46342, 47250, 47290
- **Directors**: 2 active (Zoe Brodie, Fitzroy Joseph Spencer)

### Filing Information (from API)
- **Last Accounts**: 2024-06-30 (filed 2025-05-19)
- **Account Type**: micro-entity
- **Next Due**: 2026-03-31
- **Filing Status**: Current (not overdue)
- **Total Filings**: 6 accounts since incorporation

### Financial Metrics (from iXBRL parsing)

✅ **Balance Sheet Data Available:**
| Metric | Value | Notes |
|--------|-------|-------|
| Fixed Assets | £53,468 | Property, equipment, etc. |
| Current Assets | £84,731 | Cash, inventory, etc. |
| Net Current Assets | £8,788 | Current assets - liabilities |
| Total Assets | £62,256 | Total assets less liabilities |
| Net Assets | £32,747 | Net worth of business |
| Shareholders' Equity | £32,747 | Owner's stake in business |

❌ **NOT Disclosed (Micro-Entity Exemption):**
- Turnover / Revenue
- Profit / Loss
- Cost of sales
- Number of employees
- Directors' remuneration
- Detailed P&L breakdown

---

## Key Findings

### 1. Account Types Distribution (102 Companies)

Based on our Companies House data:
- **91 companies** are "ltd" (private limited)
- **2 companies** are "plc" (public - full disclosure)
- **1 company** is "llp" (limited liability partnership)
- **5 companies** are "private-limited-guarant-nsc"

**Expected Account Types:**
- ~70-80% will file as **micro-entity** (minimal disclosure)
- ~15-20% will file as **small company** (partial disclosure)
- ~5-10% will file as **full accounts** (complete disclosure)

### 2. What Data We Can Get

#### Phase 1: Filing Metadata (100% Coverage)
From Companies House API directly:

```python
{
    "last_accounts_date": "2024-06-30",
    "account_type": "micro-entity",
    "filing_status": "current",
    "accounts_next_due": "2026-03-31",
    "company_age_years": 7,
    "filing_compliance": "on-time",  # derived from due dates
    "years_since_last_filing": 0.5   # freshness indicator
}
```

**Implementation**: ~2 hours
**Value**: High (company size, compliance, stability)

#### Phase 2: Financial Metrics (40-60% Useful Coverage)
From iXBRL document parsing:

**Micro-Entity Accounts** (~70-80% of companies):
```python
{
    "total_assets": 62256,          # ✅ Always present
    "net_assets": 32747,            # ✅ Always present
    "fixed_assets": 53468,          # ✅ Usually present
    "current_assets": 84731,        # ✅ Usually present
    "turnover": None,               # ❌ Exempt
    "profit_loss": None,            # ❌ Exempt
    "employees": None               # ❌ Exempt
}
```

**Small/Full Accounts** (~20-30% of companies):
```python
{
    "turnover": 450000,             # ✅ Present
    "gross_profit": 180000,         # ✅ Present
    "operating_profit": 45000,      # ✅ Present
    "profit_loss": 32000,           # ✅ Present
    "employees": 15,                # ✅ Present
    "total_assets": 225000,         # ✅ Present
    "net_assets": 125000            # ✅ Present
}
```

**Implementation**: ~8-12 hours
**Value**: Medium (limited data for most restaurants)

---

## Analysis Opportunities

### With Phase 1 (Filing Metadata) Only

**Dashboard Enhancements:**
- 📊 Filter by account type (micro/small/full)
- 📅 Show company age and incorporation date
- ✅ Filing compliance indicators
- 🏢 Company size category badges

**Business Insights:**
- Are older companies more likely to have better hygiene ratings?
- Do companies with overdue filings have worse reviews?
- Correlation between filing compliance and business stability?

**Example Display:**
```
🏢 Business Profile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Company: HONKYTONK WINE LIBRARY LIMITED
Age: 7 years (established 2018)
Size: Micro-entity (<£632k turnover)
Filing: ✅ Current (filed May 2025)
Next Due: March 2026
```

### With Phase 2 (Financial Metrics) - If Implemented

**For ~30% with Full Data:**
- Revenue vs menu pricing correlation
- Profit margins vs price range
- Asset size vs restaurant capacity
- Employee count vs service quality

**For ~70% with Limited Data:**
- Net assets as proxy for business stability
- Asset growth over time
- Balance sheet strength indicators

**Example Display:**
```
💰 Financial Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Net Assets: £32,747
Total Assets: £62,256
Financial Position: Stable
Last Updated: June 2024

⚠️ Note: Full financial details not disclosed
    (micro-entity exemption)
```

---

## Recommendation

### ✅ **Implement Phase 1: Filing Metadata**

**Why:**
1. **Easy to implement** - Pure API calls, no document parsing
2. **100% coverage** - Works for all 102 companies
3. **High data quality** - Structured, reliable data
4. **Immediate value** - Company size, age, compliance
5. **Foundation for future** - Can add Phase 2 later

**What to Build:**
```python
fetch_filing_metadata.py:
- For each of 102 companies with company_number
- Call Companies House API /company/{number}
- Extract accounts metadata from response
- Update database with 5 new columns
- Export summary CSV for review
- Run time: ~2 minutes for all companies
```

**Database Schema:**
```sql
ALTER TABLE restaurants ADD COLUMN last_accounts_date TEXT;
ALTER TABLE restaurants ADD COLUMN account_type TEXT;
ALTER TABLE restaurants ADD COLUMN filing_status TEXT;
ALTER TABLE restaurants ADD COLUMN accounts_next_due TEXT;
ALTER TABLE restaurants ADD COLUMN filing_metadata_fetched_at TEXT;
```

**Dashboard Updates:**
- Add filing info to Restaurant Profiles tab
- Add company size badge to restaurant cards
- Add filing status indicator
- Show company age prominently

### ⚠️ **Phase 2: Consider Later**

**Only implement if:**
- You need asset data specifically
- You're willing to accept 40-60% useful coverage
- You have time for complex iXBRL parsing
- You want full financial data for the ~30% that disclose it

**Alternative:** Wait until more companies file full/small accounts

---

## Sample Data: What Users Will See

### Phase 1 Implementation:

**Restaurant Card Badge:**
```
🏢 HONKYTONK WINE LIBRARY LIMITED
⭐⭐⭐⭐⭐ Hygiene Rating: 5
📊 Micro-entity (7 years)
✅ Filing: Current
💬 4.2★ (15 reviews)
```

**Restaurant Profile:**
```
═══════════════════════════════════════════════
🏢 Business Information
═══════════════════════════════════════════════

Company: HONKYTONK WINE LIBRARY LIMITED
Number: 11403510 (view on Companies House ↗)
Status: ✅ Active
Type: Private Limited Company

📊 Company Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 7 years (incorporated June 2018)
Size: Micro-entity (<£632k turnover limit)
Filing: ✅ Current (filed May 2025)
Next Due: March 2026

👥 Directors
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Zoe Brodie - Director
• Fitzroy Joseph Spencer - Director

Data from Companies House, fetched November 2025
```

---

## Next Steps

If proceeding with **Phase 1**:

1. ✅ **Create implementation script** (`fetch_filing_metadata.py`)
2. ✅ **Update database schema** (5 new columns)
3. ✅ **Fetch metadata for 102 companies** (~2 min runtime)
4. ✅ **Update dashboard** (Restaurant Profiles tab)
5. ✅ **Test with multiple companies** (micro, small, full accounts)
6. ✅ **Document and commit**

**Time Estimate**: 2-3 hours total

---

## POC Files Created

1. `poc_financial_data.py` - Initial discovery (company profile + filing history)
2. `poc_download_accounts.py` - Document download test
3. `poc_parse_ixbrl.py` - iXBRL parsing and data extraction
4. `honkytonks_accounts_2024.pdf` - Downloaded accounts (31 KB)
5. `honkytonks_accounts_2024.html` - Downloaded iXBRL (34 KB)
6. `FINANCIAL_DATA_POC_SUMMARY.md` - This document

---

## References

- **Companies House API**: https://developer.company-information.service.gov.uk/
- **Micro-entity Accounts**: https://www.gov.uk/prepare-file-annual-accounts-for-limited-company
- **Account Exemptions**: https://www.gov.uk/annual-accounts/microentities-small-and-dormant-companies
- **iXBRL Taxonomy**: https://www.frc.org.uk/accountants/accounting-and-reporting-policy/uk-accounting-standards/frs-102-the-financial-reporting-standard-applicable-in-the-uk-and-republic-of-ireland

---

**POC Status**: ✅ Complete
**Recommendation**: Implement Phase 1 (Filing Metadata)
**Next Action**: Build `fetch_filing_metadata.py` and update database
