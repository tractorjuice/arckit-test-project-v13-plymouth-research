#!/usr/bin/env python3
"""
Interactive Data Matcher

Allows manual review and selection of matches for restaurants with missing data.
Shows top 5 potential matches for each restaurant and lets user select the correct one.

Supports:
- Licensing data (170 unmatched)
- FSA Hygiene ratings (56 unmatched)
- Business Rates (179 unmatched)

Author: Claude Code
Date: 2025-11-22
"""

import sqlite3
import json
import re
import difflib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def normalize_business_name(name: str) -> str:
    """Normalize business name for better matching."""
    if not name or pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # Remove corporate suffixes
    corporate_patterns = [
        r'\s+LIMITED\s*$', r'\s+LTD\.?\s*$', r'\s+PLC\.?\s*$',
        r'\s+HOLDINGS?\s*$', r'\s+\(UK\)\s*$', r'\s+UK\s*$',
        r'\s+GROUP\s*$', r'\s+RESTAURANTS?\s*$',
    ]
    for pattern in corporate_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove location suffixes
    location_patterns = [
        r'\s+PLYMOUTH\s*$', r'\s+\(PLYMOUTH\)\s*$', r'\s+-\s+PLYMOUTH\s*$',
    ]
    for pattern in location_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Remove special characters except &
    name = re.sub(r'[^\w\s&#]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def calculate_name_similarity(name1: str, name2: str) -> float:
    """Calculate similarity between two names (0-100)."""
    norm1 = normalize_business_name(name1)
    norm2 = normalize_business_name(name2)

    if not norm1 or not norm2:
        return 0.0

    return difflib.SequenceMatcher(None, norm1, norm2).ratio() * 100

def extract_postcode(text: str) -> Optional[str]:
    """Extract UK postcode from text."""
    if not text:
        return None

    pattern = r'[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}'
    match = re.search(pattern, text.upper())

    if match:
        postcode = match.group(0).replace(' ', '')
        return f"{postcode[:-3]} {postcode[-3:]}"

    return None

class InteractiveMatcher:
    def __init__(self, data_source: str):
        """
        Initialize interactive matcher.

        Args:
            data_source: 'licensing', 'fsa', or 'business_rates'
        """
        self.data_source = data_source
        self.db_path = 'plymouth_research.db'
        self.verified_matches = []
        self.skipped = []

        # Load data based on source
        if data_source == 'licensing':
            self.load_licensing_data()
        elif data_source == 'fsa':
            self.load_fsa_data()
        elif data_source == 'business_rates':
            self.load_business_rates_data()
        else:
            raise ValueError(f"Unknown data source: {data_source}")

    def load_licensing_data(self):
        """Load licensing data."""
        # Load unmatched restaurants
        unmatched_df = pd.read_csv('licensing_unmatched.csv')
        self.unmatched_restaurants = unmatched_df.to_dict('records')

        # Load all licensing premises
        with open('plymouth_licensing_complete_fixed.json', 'r') as f:
            self.source_data = json.load(f)

        self.total_unmatched = len(self.unmatched_restaurants)
        print(f"\n{Colors.OKGREEN}Loaded {self.total_unmatched} unmatched restaurants{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Loaded {len(self.source_data)} licensing premises{Colors.ENDC}")

    def load_fsa_data(self):
        """Load FSA hygiene data."""
        # Load unmatched restaurants
        unmatched_df = pd.read_csv('fsa_hygiene_unmatched_v2.csv')
        self.unmatched_restaurants = unmatched_df.to_dict('records')

        # Load FSA establishments
        # Note: You'll need to have the FSA XML parsed to JSON or CSV
        # For now, using a placeholder
        print(f"{Colors.WARNING}FSA data loader not implemented yet{Colors.ENDC}")
        self.source_data = []
        self.total_unmatched = len(self.unmatched_restaurants)

    def load_business_rates_data(self):
        """Load business rates data."""
        # Load unmatched restaurants
        unmatched_df = pd.read_csv('business_rates_unmatched_v3.csv')
        self.unmatched_restaurants = unmatched_df.to_dict('records')

        # Load business rates data
        rates_df = pd.read_csv('plymouth_business_rates_2025.csv')
        self.source_data = rates_df.to_dict('records')

        self.total_unmatched = len(self.unmatched_restaurants)
        print(f"\n{Colors.OKGREEN}Loaded {self.total_unmatched} unmatched restaurants{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Loaded {len(self.source_data)} business rates records{Colors.ENDC}")

    def find_top_matches(self, restaurant: Dict, n: int = 5) -> List[Dict]:
        """Find top N matches for a restaurant."""
        rest_name = restaurant['restaurant_name']
        rest_address = restaurant.get('restaurant_address', '')
        rest_postcode = restaurant.get('restaurant_postcode', '')

        matches = []

        for source_item in self.source_data:
            if self.data_source == 'licensing':
                source_name = source_item.get('name', '')
                source_address = source_item.get('address', '')
            elif self.data_source == 'business_rates':
                source_name = source_item.get('Account Holder', '')
                source_address = source_item.get('Full Property Address', '')
            else:
                continue

            # Calculate similarity
            name_sim = calculate_name_similarity(rest_name, source_name)

            # Calculate address similarity (simple word overlap)
            addr_score = 0
            if rest_address and source_address:
                rest_words = set(normalize_business_name(rest_address).split())
                source_words = set(normalize_business_name(source_address).split())
                common = rest_words & source_words
                addr_score = len(common) * 5

            # Postcode match
            postcode_match = False
            source_postcode = extract_postcode(source_address)
            if rest_postcode and source_postcode:
                if rest_postcode.replace(' ', '').upper() == source_postcode.replace(' ', '').upper():
                    postcode_match = True

            total_score = name_sim + addr_score + (30 if postcode_match else 0)

            matches.append({
                'source_item': source_item,
                'source_name': source_name,
                'source_address': source_address,
                'name_similarity': name_sim,
                'address_score': addr_score,
                'postcode_match': postcode_match,
                'total_score': total_score
            })

        # Sort by total score descending
        matches.sort(key=lambda x: x['total_score'], reverse=True)

        return matches[:n]

    def display_restaurant(self, restaurant: Dict, idx: int):
        """Display restaurant details."""
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Restaurant {idx + 1}/{self.total_unmatched}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}ID:{Colors.ENDC} {restaurant['restaurant_id']}")
        print(f"{Colors.OKBLUE}Name:{Colors.ENDC} {restaurant['restaurant_name']}")
        print(f"{Colors.OKBLUE}Address:{Colors.ENDC} {restaurant.get('restaurant_address', 'N/A')}")
        print(f"{Colors.OKBLUE}Postcode:{Colors.ENDC} {restaurant.get('restaurant_postcode', 'N/A')}")

    def display_matches(self, matches: List[Dict]):
        """Display top matches."""
        print(f"\n{Colors.OKCYAN}Top 5 Potential Matches:{Colors.ENDC}")
        print(f"{Colors.HEADER}{'-'*80}{Colors.ENDC}")

        for i, match in enumerate(matches, 1):
            score_color = Colors.OKGREEN if match['total_score'] >= 70 else Colors.WARNING

            print(f"\n{Colors.BOLD}[{i}]{Colors.ENDC} {score_color}Score: {match['total_score']:.1f}{Colors.ENDC}")
            print(f"    Name: {match['source_name']}")
            print(f"    Address: {match['source_address']}")
            print(f"    Match: name={match['name_similarity']:.0f}%, "
                  f"postcode={'✓' if match['postcode_match'] else '✗'}, "
                  f"address={match['address_score']}")

            # Show specific details based on data source
            if self.data_source == 'licensing':
                details = match['source_item'].get('details', {})
                license_num = details.get('license_number', 'N/A')
                activities = details.get('licensable_activities', [])
                print(f"    License: {license_num}")
                if activities:
                    print(f"    Activities: {', '.join(activities[:3])}")

            elif self.data_source == 'business_rates':
                rv = match['source_item'].get('Rateable Value 2023', 'N/A')
                category = match['source_item'].get('Primary Liable party Description', 'N/A')
                print(f"    Rateable Value: £{rv:,}" if rv != 'N/A' else f"    Rateable Value: N/A")
                print(f"    Category: {category}")

    def get_user_choice(self) -> Tuple[Optional[int], bool]:
        """
        Get user's choice.

        Returns:
            (selection, quit_flag) - selection is 1-5 or None for skip, quit_flag is True to exit
        """
        print(f"\n{Colors.OKCYAN}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Options:{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}1-5:{Colors.ENDC} Select match")
        print(f"  {Colors.WARNING}s:{Colors.ENDC} Skip this restaurant")
        print(f"  {Colors.WARNING}q:{Colors.ENDC} Quit and save progress")
        print(f"  {Colors.WARNING}n:{Colors.ENDC} None of these match")

        while True:
            choice = input(f"\n{Colors.BOLD}Your choice: {Colors.ENDC}").strip().lower()

            if choice == 'q':
                return None, True
            elif choice == 's' or choice == 'n':
                return None, False
            elif choice in ['1', '2', '3', '4', '5']:
                return int(choice), False
            else:
                print(f"{Colors.FAIL}Invalid choice. Please enter 1-5, s, n, or q{Colors.ENDC}")

    def save_progress(self):
        """Save verified matches and skipped restaurants."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if self.verified_matches:
            # Convert to DataFrame and save
            df = pd.DataFrame(self.verified_matches)
            filename = f'{self.data_source}_manual_matches_{timestamp}.csv'
            df.to_csv(filename, index=False)
            print(f"\n{Colors.OKGREEN}✓ Saved {len(self.verified_matches)} verified matches to {filename}{Colors.ENDC}")

        if self.skipped:
            df = pd.DataFrame(self.skipped)
            filename = f'{self.data_source}_manual_skipped_{timestamp}.csv'
            df.to_csv(filename, index=False)
            print(f"{Colors.WARNING}✓ Saved {len(self.skipped)} skipped restaurants to {filename}{Colors.ENDC}")

    def run(self):
        """Run interactive matching session."""
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}INTERACTIVE {self.data_source.upper()} MATCHER{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"\nReviewing {self.total_unmatched} unmatched restaurants")
        print(f"For each restaurant, you'll see the top 5 potential matches")
        print(f"Select the correct match or skip if none match")

        for idx, restaurant in enumerate(self.unmatched_restaurants):
            # Display restaurant
            self.display_restaurant(restaurant, idx)

            # Find and display top matches
            top_matches = self.find_top_matches(restaurant, n=5)

            if not top_matches:
                print(f"\n{Colors.WARNING}No potential matches found{Colors.ENDC}")
                continue

            self.display_matches(top_matches)

            # Get user choice
            selection, quit_flag = self.get_user_choice()

            if quit_flag:
                print(f"\n{Colors.WARNING}Quitting and saving progress...{Colors.ENDC}")
                break

            if selection is not None:
                # User selected a match
                selected_match = top_matches[selection - 1]

                # Build verified match record
                match_record = {
                    'restaurant_id': restaurant['restaurant_id'],
                    'restaurant_name': restaurant['restaurant_name'],
                    'restaurant_address': restaurant.get('restaurant_address', ''),
                    'restaurant_postcode': restaurant.get('restaurant_postcode', ''),
                    'match_confidence': selected_match['total_score'],
                    'match_reason': 'manual_selection',
                }

                # Add source-specific fields
                if self.data_source == 'licensing':
                    source_item = selected_match['source_item']
                    details = source_item.get('details', {})
                    match_record.update({
                        'premises_id': source_item.get('premises_id'),
                        'premises_name': source_item.get('name'),
                        'premises_address': source_item.get('address'),
                        'license_number': details.get('license_number'),
                        'license_url': details.get('license_url'),
                        'dps_name': details.get('dps_name'),
                        'licensable_activities': json.dumps(details.get('licensable_activities', [])),
                        'opening_hours': json.dumps(details.get('opening_hours', [])),
                    })

                elif self.data_source == 'business_rates':
                    source_item = selected_match['source_item']
                    match_record.update({
                        'business_rates_account_holder': source_item.get('Account Holder'),
                        'business_rates_address': source_item.get('Full Property Address'),
                        'business_rates_postcode': source_item.get('Postcode'),
                        'business_rates_rateable_value': source_item.get('Rateable Value 2023'),
                        'business_rates_category': source_item.get('Primary Liable party Description'),
                    })

                self.verified_matches.append(match_record)
                print(f"{Colors.OKGREEN}✓ Match recorded{Colors.ENDC}")
            else:
                # User skipped
                self.skipped.append(restaurant)
                print(f"{Colors.WARNING}⊘ Skipped{Colors.ENDC}")

        # Save progress
        self.save_progress()

        # Summary
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}SESSION SUMMARY{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"Restaurants reviewed: {idx + 1}/{self.total_unmatched}")
        print(f"{Colors.OKGREEN}Verified matches: {len(self.verified_matches)}{Colors.ENDC}")
        print(f"{Colors.WARNING}Skipped: {len(self.skipped)}{Colors.ENDC}")

        if self.verified_matches:
            print(f"\n{Colors.BOLD}Next steps:{Colors.ENDC}")
            print(f"1. Review the verified matches CSV")
            print(f"2. Run the appropriate import script to update the database")
            print(f"3. Verify updates in dashboard")

def main():
    """Main entry point."""
    print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}INTERACTIVE DATA MATCHER{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"\nSelect data source to match:")
    print(f"  {Colors.OKGREEN}1.{Colors.ENDC} Licensing data (170 unmatched)")
    print(f"  {Colors.OKGREEN}2.{Colors.ENDC} Business Rates (179 unmatched)")
    print(f"  {Colors.OKGREEN}3.{Colors.ENDC} FSA Hygiene (56 unmatched)")

    while True:
        choice = input(f"\n{Colors.BOLD}Your choice (1-3): {Colors.ENDC}").strip()

        if choice == '1':
            data_source = 'licensing'
            break
        elif choice == '2':
            data_source = 'business_rates'
            break
        elif choice == '3':
            data_source = 'fsa'
            break
        else:
            print(f"{Colors.FAIL}Invalid choice. Please enter 1, 2, or 3{Colors.ENDC}")

    # Run interactive matcher
    matcher = InteractiveMatcher(data_source)
    matcher.run()

if __name__ == "__main__":
    main()
