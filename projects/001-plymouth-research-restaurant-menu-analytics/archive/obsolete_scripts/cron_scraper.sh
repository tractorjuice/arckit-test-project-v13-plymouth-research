#!/bin/bash
#
# Cron Job Script for Automated Restaurant Scraping
# ==================================================
#
# This script is designed to be run by cron on a schedule.
# It runs the automated scraper and emails results if configured.
#
# Installation:
#   1. Make executable: chmod +x cron_scraper.sh
#   2. Add to crontab: crontab -e
#   3. Add line: 0 2 * * 0 /path/to/cron_scraper.sh
#      (Runs every Sunday at 2am)
#
# Author: Plymouth Research Team
# Date: 2025-11-17

# Set working directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Log file
LOG_FILE="$SCRIPT_DIR/scraper_cron.log"

# Run scraper with timestamp
echo "========================================" >> "$LOG_FILE"
echo "Scraper started: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

python src/scrapers/automated_scraper.py >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "Scraper completed: $(date)" >> "$LOG_FILE"
echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Optional: Send email notification (requires mailx)
# if [ $EXIT_CODE -ne 0 ]; then
#     echo "Scraper failed" | mail -s "Plymouth Scraper Alert" admin@example.com
# fi

exit $EXIT_CODE
