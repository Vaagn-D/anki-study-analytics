#!/usr/bin/env python3
"""
Extract daily review counts from Anki collection.anki2 database
Exports data from June 11, 2023 onwards
"""

import os
import sqlite3
import csv
from datetime import datetime, date, timedelta

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DB_PATH = "/Users/vahagdanielian/Desktop/collection.anki2"
OUTPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'anki_daily_reviews.csv')

# June 11, 2023
START_DATE = date(2023, 6, 11)
# June 11, 2023, 00:00:00 UTC in milliseconds
START_DATE_MS = 1686441600000

def extract_daily_reviews():
    """Extract daily review counts from Anki database"""

    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQL query to get daily review counts by type
    # Type 0 = Learning (new cards), 1 = Review (graduated cards), 2 = Relearn (failed review cards)
    # Excludes: 3 (Filtered/Cram), 4 (unknown/manual)
    # Using 'localtime' to convert to local timezone (Moscow time)
    query = """
    SELECT
        DATE(id/1000, 'unixepoch', 'localtime') as review_date,
        SUM(CASE WHEN type = 0 THEN 1 ELSE 0 END) as learning,
        SUM(CASE WHEN type = 1 THEN 1 ELSE 0 END) as review,
        SUM(CASE WHEN type = 2 THEN 1 ELSE 0 END) as relearn,
        COUNT(*) as total
    FROM revlog
    WHERE id >= ?
    AND type IN (0, 1, 2)
    GROUP BY DATE(id/1000, 'unixepoch', 'localtime')
    ORDER BY review_date
    """

    print(f"Executing query for data from June 11, 2023 onwards...")
    cursor.execute(query, (START_DATE_MS,))

    # Fetch all results into a dictionary
    # Structure: {date: (learning, review, relearn, total)}
    review_data = {row[0]: (row[1], row[2], row[3], row[4]) for row in cursor.fetchall()}
    conn.close()

    print(f"Found {len(review_data)} days with actual reviews")

    # Generate complete date range from START_DATE to today
    today = date.today()
    current_date = START_DATE
    all_dates = []

    while current_date <= today:
        date_str = current_date.strftime('%Y-%m-%d')
        # Get (learning, review, relearn, total) or (0, 0, 0, 0) if no reviews
        data = review_data.get(date_str, (0, 0, 0, 0))
        all_dates.append((date_str, data[0], data[1], data[2], data[3]))
        current_date += timedelta(days=1)

    print(f"Generated complete date range: {len(all_dates)} days total")

    # Write to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Learning', 'Review', 'Relearn', 'Total'])
        writer.writerows(all_dates)

    results = all_dates

    print(f"\nData exported to: {OUTPUT_CSV}")
    print(f"Total days: {len(results)}")

    # Show first and last 5 rows as preview
    if results:
        print("\n--- First 5 days ---")
        for row in results[:5]:
            print(f"{row[0]}: Learning={row[1]}, Review={row[2]}, Relearn={row[3]}, Total={row[4]}")

        if len(results) > 10:
            print("\n--- Last 5 days ---")
            for row in results[-5:]:
                print(f"{row[0]}: Learning={row[1]}, Review={row[2]}, Relearn={row[3]}, Total={row[4]}")

        # Calculate statistics
        total_learning = sum(row[1] for row in results)
        total_review = sum(row[2] for row in results)
        total_relearn = sum(row[3] for row in results)
        total_reviews = sum(row[4] for row in results)
        days_with_reviews = sum(1 for row in results if row[4] > 0)
        days_without_reviews = len(results) - days_with_reviews

        print(f"\n--- Statistics ---")
        print(f"Total Learning: {total_learning:,} cards")
        print(f"Total Review: {total_review:,} cards")
        print(f"Total Relearn: {total_relearn:,} cards")
        print(f"Total reviews: {total_reviews:,} cards")
        print(f"Days with reviews: {days_with_reviews}")
        print(f"Days without reviews (0 cards): {days_without_reviews}")
        print(f"Average per day (all days): {total_reviews / len(results):.1f} cards")
        if days_with_reviews > 0:
            print(f"Average per active day: {total_reviews / days_with_reviews:.1f} cards")

    return results

if __name__ == "__main__":
    try:
        extract_daily_reviews()
        print("\n✓ Export completed successfully!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
