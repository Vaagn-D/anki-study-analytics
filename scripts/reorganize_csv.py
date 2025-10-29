#!/usr/bin/env python3
"""
Reorganize Anki daily reviews CSV to show honest metrics
Total = Learning + Review - Cheated (real work, without relearning, without cheating)
Relearn = separate metric for effort/difficulty
Cheated = cheating metric (cards answered in <1 second)
"""

import os
import csv

# File paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

INPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'anki_daily_reviews.csv')
OUTPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'anki_daily_reviews_honest.csv')

def reorganize_csv():
    """
    Read the original CSV and create a new one with reorganized columns
    Original: Date, Learning, Review, Relearn, Total, AvgTime, MedianTime, FastCount, FastPercent
    New: Date, Learning, Review, Relearn, Cheated, Total
    Where Total = Learning + Review - Cheated (honest work without relearn, without cheating)
    Removed: AvgTime, MedianTime, FastPercent (not needed)
    """

    print(f"Reading from: {INPUT_CSV}")

    rows_processed = 0
    with open(INPUT_CSV, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write new header
        header = next(reader)  # Read original header
        new_header = ['Date', 'Learning', 'Review', 'Relearn', 'Cheated', 'Total']
        writer.writerow(new_header)
        print(f"Original header: {header}")
        print(f"New header: {new_header}\n")

        # Process each row
        for row in reader:
            date = row[0]
            learning = int(row[1])
            review = int(row[2])
            relearn = int(row[3])
            # old_total = int(row[4])  # Not used
            # avg_time = float(row[5])  # Not used
            # median_time = float(row[6])  # Not used
            cheated = int(row[7])
            # fast_percent = float(row[8])  # Not used

            # Calculate honest total (Learning + Review - Cheated)
            honest_total = learning + review - cheated

            # Write new row: Date, Learning, Review, Relearn, Cheated, Total
            new_row = [date, learning, review, relearn, cheated, honest_total]
            writer.writerow(new_row)
            rows_processed += 1

    print(f"Processed {rows_processed} rows")
    print(f"Output saved to: {OUTPUT_CSV}")

    # Show examples
    print("\n--- First 5 rows ---")
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for i, row in enumerate(reader):
            if i >= 5:
                break
            print(f"{row[0]}: L={row[1]:>3} R={row[2]:>3} Re={row[3]:>3} Cheated={row[4]:>3} Total={row[5]:>3}")

    print("\n--- Last 5 rows ---")
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[-5:]:
            row = line.strip().split(',')
            if len(row) >= 6:
                print(f"{row[0]}: L={row[1]:>3} R={row[2]:>3} Re={row[3]:>3} Cheated={row[4]:>3} Total={row[5]:>3}")

    # Calculate statistics
    print("\n--- Statistics ---")
    total_learning = 0
    total_review = 0
    total_relearn = 0
    total_cheated = 0
    total_honest = 0
    days_with_work = 0

    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            learning = int(row[1])
            review = int(row[2])
            relearn = int(row[3])
            cheated = int(row[4])
            honest_total = int(row[5])

            total_learning += learning
            total_review += review
            total_relearn += relearn
            total_cheated += cheated
            total_honest += honest_total

            if honest_total > 0:
                days_with_work += 1

    total_days = rows_processed

    print(f"Total Learning: {total_learning:,}")
    print(f"Total Review: {total_review:,}")
    print(f"Total Relearn (separate): {total_relearn:,} cards")
    print(f"Total Cheated (removed): {total_cheated:,} cards")
    print(f"Total honest work (L+R-Cheated): {total_honest:,} cards")
    print(f"Days with work: {days_with_work}/{total_days}")
    print(f"Average per day (all): {total_honest / total_days:.1f} cards")
    print(f"Average per active day: {total_honest / days_with_work:.1f} cards")

    print("\n✅ Done! New file created with honest metrics.")

if __name__ == "__main__":
    reorganize_csv()
