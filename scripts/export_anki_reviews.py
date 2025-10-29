#!/usr/bin/env python3
"""
Extract daily review counts from Anki collection.anki2 database
Exports data from June 11, 2023 onwards
Includes time metrics: avg time, median time, fast reviews count
"""

import os
import sqlite3
import csv
from datetime import datetime, date, timedelta
from collections import defaultdict
import statistics

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DB_PATH = "/Users/vahagdanielian/Desktop/collection.anki2"
OUTPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'anki_daily_reviews.csv')

# June 11, 2023
START_DATE = date(2023, 6, 11)
# June 11, 2023, 00:00:00 UTC in milliseconds
START_DATE_MS = 1686441600000

# Fast review threshold (in milliseconds)
FAST_THRESHOLD_MS = 1000  # < 1 second

def extract_daily_reviews():
    """Extract daily review counts and time metrics from Anki database"""

    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQL query to get individual review records with time
    # Type 0 = Learning (new cards), 1 = Review (graduated cards), 2 = Relearn (failed review cards)
    # Excludes: 3 (Filtered/Cram), 4 (unknown/manual)
    # Using 'localtime' to convert to local timezone (Moscow time)
    # time column is in milliseconds
    query = """
    SELECT
        DATE(id/1000, 'unixepoch', 'localtime') as review_date,
        type,
        time
    FROM revlog
    WHERE id >= ?
    AND type IN (0, 1, 2)
    ORDER BY review_date
    """

    print(f"Executing query for data from June 11, 2023 onwards...")
    cursor.execute(query, (START_DATE_MS,))

    # Group reviews by date and collect times
    # Structure: {date: {'learning': count, 'review': count, 'relearn': count, 'times': [time1, time2, ...]}}
    daily_data = defaultdict(lambda: {'learning': 0, 'review': 0, 'relearn': 0, 'times': []})

    for row in cursor.fetchall():
        review_date = row[0]
        review_type = row[1]
        review_time = row[2]  # in milliseconds

        # Count by type
        if review_type == 0:
            daily_data[review_date]['learning'] += 1
        elif review_type == 1:
            daily_data[review_date]['review'] += 1
        elif review_type == 2:
            daily_data[review_date]['relearn'] += 1

        # Collect time
        daily_data[review_date]['times'].append(review_time)

    conn.close()
    print(f"Found {len(daily_data)} days with actual reviews")

    # Generate complete date range from START_DATE to today with time metrics
    today = date.today()
    current_date = START_DATE
    all_dates = []

    print("Calculating time metrics for each day...")
    while current_date <= today:
        date_str = current_date.strftime('%Y-%m-%d')

        if date_str in daily_data:
            data = daily_data[date_str]
            learning = data['learning']
            review = data['review']
            relearn = data['relearn']
            total = learning + review + relearn
            times = data['times']

            # Calculate time metrics
            if len(times) > 0:
                # Convert to seconds
                times_seconds = [t / 1000.0 for t in times]
                avg_time = sum(times_seconds) / len(times_seconds)
                median_time = statistics.median(times_seconds)

                # Count fast reviews (< threshold)
                fast_count = sum(1 for t in times if t < FAST_THRESHOLD_MS)
                fast_percent = (fast_count / len(times)) * 100
            else:
                avg_time = 0.0
                median_time = 0.0
                fast_count = 0
                fast_percent = 0.0
        else:
            # No reviews this day
            learning = 0
            review = 0
            relearn = 0
            total = 0
            avg_time = 0.0
            median_time = 0.0
            fast_count = 0
            fast_percent = 0.0

        all_dates.append((
            date_str,
            learning,
            review,
            relearn,
            total,
            round(avg_time, 2),
            round(median_time, 2),
            fast_count,
            round(fast_percent, 2)
        ))
        current_date += timedelta(days=1)

    print(f"Generated complete date range: {len(all_dates)} days total")

    # Write to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Learning', 'Review', 'Relearn', 'Total', 'AvgTime', 'MedianTime', 'FastCount', 'FastPercent'])
        writer.writerows(all_dates)

    results = all_dates

    print(f"\nData exported to: {OUTPUT_CSV}")
    print(f"Total days: {len(results)}")

    # Show first and last 5 rows as preview
    if results:
        print("\n--- First 5 days ---")
        for row in results[:5]:
            print(f"{row[0]}: L={row[1]:3} R={row[2]:3} Re={row[3]:3} Total={row[4]:3} | "
                  f"Avg={row[5]:5.1f}s Med={row[6]:5.1f}s Fast={row[7]:3} ({row[8]:5.1f}%)")

        if len(results) > 10:
            print("\n--- Last 5 days ---")
            for row in results[-5:]:
                print(f"{row[0]}: L={row[1]:3} R={row[2]:3} Re={row[3]:3} Total={row[4]:3} | "
                      f"Avg={row[5]:5.1f}s Med={row[6]:5.1f}s Fast={row[7]:3} ({row[8]:5.1f}%)")

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
