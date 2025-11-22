# Data Importers

Scripts for importing matched data into the database.

## Active Scripts

- **import_fsa_manual_matches.py** - Import manual FSA hygiene matches
- **import_licensing_matches.py** - Import licensing matches
- **import_manual_matches_comprehensive.py** - Comprehensive manual match importer
- **import_business_rates.py** - Import business rates data
- **import_companies_house_data.py** - Import Companies House data
- **import_licensing_data.py** - Import licensing data
- **import_from_json.py** - Generic JSON importer

## Usage

All importers read from `data/manual_matches/` or `data/processed/` and update `plymouth_research.db`.

Example:
```bash
python import_fsa_manual_matches.py data/manual_matches/fsa_manual_matches_20251122_134550.csv
```
