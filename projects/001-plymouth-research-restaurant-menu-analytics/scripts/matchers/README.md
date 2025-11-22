# Data Matchers

Scripts for matching restaurant records across different data sources.

## Active Scripts

- **match_business_rates_v3.py** - Business rates matching (v3 - latest)
- **match_fsa_hygiene_v2.py** - FSA hygiene data matching (v2)
- **match_licensing_data.py** - Licensing data matching
- **interactive_matcher.py** - Old CLI interactive matcher (deprecated - use interactive_matcher_app.py)

## Usage

Matchers read from `data/raw/` and output matches to `data/processed/`.

Example:
```bash
python match_business_rates_v3.py
```
