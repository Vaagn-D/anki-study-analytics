#!/usr/bin/env python3
"""
Plot Anki review data over time
Aggregated by month with 4 lines: Learning, Review, Total, Relearn
"""

import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import defaultdict
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# File paths (relative to project root)
input_csv = os.path.join(project_root, 'data', 'anki_daily_reviews_honest.csv')
output_file = os.path.join(project_root, 'output', 'anki_review_plot.png')

# Read CSV file
data_by_month = defaultdict(lambda: {'learning': 0, 'review': 0, 'total': 0, 'relearn': 0})

print(f"Reading data from: {input_csv}")
with open(input_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    for row in reader:
        date_str = row[0]
        learning = int(row[1])
        review = int(row[2])
        total = int(row[3])
        relearn = int(row[4])

        # Get year-month key
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month_key = date_obj.strftime('%Y-%m')

        # Aggregate by month
        data_by_month[month_key]['learning'] += learning
        data_by_month[month_key]['review'] += review
        data_by_month[month_key]['total'] += total
        data_by_month[month_key]['relearn'] += relearn

# Sort by date
sorted_months = sorted(data_by_month.keys())

# Prepare data for plotting
dates = [datetime.strptime(month, '%Y-%m') for month in sorted_months]
learning_values = [data_by_month[month]['learning'] for month in sorted_months]
review_values = [data_by_month[month]['review'] for month in sorted_months]
total_values = [data_by_month[month]['total'] for month in sorted_months]
relearn_values = [data_by_month[month]['relearn'] for month in sorted_months]

# Create plot
plt.figure(figsize=(16, 8))

plt.plot(dates, learning_values, color='blue', linewidth=2, label='Learning (New Cards)', marker='o', markersize=4)
plt.plot(dates, review_values, color='green', linewidth=2, label='Review', marker='s', markersize=4)
plt.plot(dates, total_values, color='gray', linewidth=3, label='Total (Learning + Review)', marker='D', markersize=4, alpha=0.7)
plt.plot(dates, relearn_values, color='red', linewidth=2, label='Relearn (Failed Cards)', marker='^', markersize=4)

# Formatting
plt.xlabel('Date', fontsize=14, fontweight='bold')
plt.ylabel('Number of Cards', fontsize=14, fontweight='bold')
plt.title('Anki Review Activity Over Time (Monthly Aggregation)\nJune 2023 - October 2025', fontsize=16, fontweight='bold')
plt.legend(loc='upper left', fontsize=12, framealpha=0.9)
plt.grid(True, alpha=0.3, linestyle='--')

# Format x-axis dates with month names
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Sep 2023, Oct 2023, etc.
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45, ha='right')

# Add some padding
plt.tight_layout()

# Save plot
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✅ Plot saved to: {output_file}")

# Show statistics
print(f"\n=== MONTHLY STATISTICS ===")
print(f"Total months: {len(sorted_months)}")
print(f"Date range: {sorted_months[0]} to {sorted_months[-1]}")
print(f"\nMax values:")
print(f"  Learning: {max(learning_values):,} cards")
print(f"  Review: {max(review_values):,} cards")
print(f"  Total: {max(total_values):,} cards")
print(f"  Relearn: {max(relearn_values):,} cards")

# Show interactive plot
print("\n📊 Opening interactive plot window...")
plt.show()
