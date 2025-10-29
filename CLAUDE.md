# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Anki spaced repetition analytics pipeline that extracts review data from Anki's SQLite database, processes it into "honest metrics," and generates interactive dashboards and professional PDF reports.

**Key Concept - Honest Metrics:**
- `Total = Learning + Review - Cheated` (excludes Relearn to avoid double-counting, excludes Cheated for data quality)
- `Relearn` is tracked separately as a difficulty/persistence indicator
- `Cheated` represents cards answered in <1 second (rapid clicking without genuine study)
- This formula is fundamental to the entire codebase and must never be changed

## Data Pipeline Architecture

### 1. Data Extraction (`export_anki_reviews.py`)
- **Input:** Anki SQLite database at `/Users/vahagdanielian/Desktop/collection.anki2`
- **Output:** `data/anki_daily_reviews.csv`
- **Process:**
  - Queries `revlog` table for types 0 (Learning), 1 (Review), 2 (Relearn)
  - Converts timestamps to Moscow Time (MSK, UTC+3) using localtime
  - Tracks review time in milliseconds to identify fast reviews (<1000ms)
  - Generates complete daily records from June 11, 2023 to present

### 2. Honest Metrics Transformation (`reorganize_csv.py`)
- **Input:** `data/anki_daily_reviews.csv`
- **Output:** `data/anki_daily_reviews_honest.csv`
- **Process:**
  - Maps `FastCount` column to `Cheated` (cards answered <1 second)
  - Recalculates `Total = Learning + Review - Cheated`
  - Removes time metrics (AvgTime, MedianTime, FastPercent)
  - **Final schema:** `Date, Learning, Review, Relearn, Cheated, Total`

**This is the canonical data source for all downstream analysis.**

### 3. Visualization Layer

Three independent output formats:

**A. Interactive Dashboard (`create_dashboard_tabs.py`)** ⭐ Recommended
- Uses modular architecture: `dashboard/config.py`, `dashboard/data_loader.py`, `dashboard/chart_builders.py`
- Three-tab Bootstrap 5 design (Overview, Analysis, Progress)
- Plotly-based interactive charts with zoom, pan, hover tooltips
- Output: `output/anki_dashboard.html`

**B. Static Plot (`plot_anki_data.py`)**
- Matplotlib-based monthly aggregation
- Output: `output/anki_review_plot.png`

**C. Professional PDF Report (`create_median_pdf.py`)**
- ReportLab-based business report
- **Focus:** Median comparison (typical day, not monthly aggregates)
- Compares March 2025 (best month) vs. Baseline Period (June 2023 - Oct 2025)
- **Purpose:** Template for benchmarking against future daily consistency targets
- Output: `output/march_2025_median_comparison.pdf`

## Common Commands

### Full Pipeline Update
```bash
cd scripts
python3 export_anki_reviews.py       # Extract from Anki DB
python3 reorganize_csv.py             # Transform to honest metrics
python3 create_dashboard_tabs.py     # Generate dashboard
python3 create_median_pdf.py         # Generate PDF report
```

### Individual Operations
```bash
# Dashboard only (fastest iteration)
cd scripts
python3 create_dashboard_tabs.py

# PDF report only
cd scripts
python3 create_median_pdf.py

# Static plot only
cd scripts
python3 plot_anki_data.py
```

### View Outputs
```bash
# Dashboard
open output/anki_dashboard.html

# PDF report
open output/march_2025_median_comparison.pdf

# Static plot
open output/anki_review_plot.png
```

## Code Architecture

### Modular Dashboard System

**`dashboard/config.py`** - Single source of truth for all dashboard settings
- Paths, colors, fonts, chart configurations
- Modify color scheme: `COLORS` dict
- Toggle offline mode: `INCLUDE_PLOTLYJS = True` (3.5MB) vs `'cdn'` (130KB)
- Adjust chart heights: `ROW_HEIGHTS` list (must sum to 1.0)

**`dashboard/data_loader.py`** - Data preprocessing pipeline
- `load_anki_data()`: Main entry point, returns enriched DataFrame
- Adds computed columns: moving averages, cumulative sums, streaks, activity flags
- `calculate_summary_stats()`: Key metrics for indicator cards
- `calculate_monthly_stats()`: Monthly aggregation for time series
- `prepare_heatmap_data()`: GitHub-style calendar pivot

**`dashboard/chart_builders.py`** - Plotly chart generators
- Each function creates one chart type
- All functions import settings from `config.py`
- Returns Plotly figure objects

### Data Processing Chain

```
collection.anki2 (SQLite)
    ↓ [export_anki_reviews.py]
anki_daily_reviews.csv (raw data + time metrics)
    ↓ [reorganize_csv.py]
anki_daily_reviews_honest.csv (Total = L+R-Cheated)
    ↓ [data_loader.py]
Enriched DataFrame (MA, cumulative, streaks)
    ↓ [chart_builders.py or create_median_pdf.py]
Outputs (HTML dashboard, PNG plot, PDF report)
```

### Important Data Transformations

**Moving Averages:** Applied to `Total` column only, windows defined in `config.MOVING_AVERAGES` (default: 7, 30 days)

**Streaks:** Consecutive days where `Total >= MIN_CARDS_FOR_ACTIVE_DAY` (default: 1)

**Activity Flags:**
- `IsActive`: Total >= 1 card
- `IsZero`: Total == 0

**Heatmap Pivot:** Rows = weekday (Mon-Sun), Columns = year-week, Values = Total cards

## Critical Constraints

### Data Integrity Rules

1. **Never modify the honest metrics formula:** `Total = Learning + Review - Cheated`
   - This is validated across 872 days of data
   - Relearn is intentionally excluded (avoid double-counting)
   - Cheated is intentionally excluded (data quality)

2. **Timezone consistency:** All date conversions use Moscow Time (MSK, UTC+3)
   - SQLite query uses `'localtime'` conversion
   - Do not change to UTC or other timezones

3. **Cheating threshold:** <1000ms (1 second)
   - This is the minimum physically possible time to read, think, and click
   - Do not lower this threshold

4. **Date range:** June 11, 2023 onwards (hardcoded in `export_anki_reviews.py:START_DATE_MS`)

### PDF Report Specifics

When modifying `create_median_pdf.py`:

1. **Use medians, not means** - Report focuses on "typical day" analysis
2. **Activity Rate is critical** - This metric compares intermittent (58.1%) vs. daily consistency (100% target)
3. **Benchmark Summary must include both periods** - Baseline and March 2025
4. **No emojis** - Professional business format only
5. **English only** - ReportLab cannot render Cyrillic without special fonts
6. **Interpretation of median Cheated = 0** - Means >50% of days were clean, NOT related to Total normalization

### Dashboard Customization

When modifying dashboards:

1. **Always run scripts from `scripts/` directory** - Import paths assume this
2. **Row heights must sum to 1.0** - `config.ROW_HEIGHTS` list
3. **Color changes:** Edit `config.COLORS` dict, not individual chart functions
4. **CDN vs. Embedded:** `config.INCLUDE_PLOTLYJS = 'cdn'` for web sharing (requires internet), `True` for offline (3.5MB file)

## Data Source Location

**Anki Database Path (macOS):** `/Users/vahagdanielian/Desktop/collection.anki2`

To update this path (different user/platform):
1. Edit `scripts/export_anki_reviews.py:DB_PATH`
2. Standard locations:
   - macOS: `~/Library/Application Support/Anki2/[Profile]/collection.anki2`
   - Windows: `%APPDATA%\Anki2\[Profile]\collection.anki2`
   - Linux: `~/.local/share/Anki2/[Profile]/collection.anki2`

## Median vs Mean Analysis

**Why the PDF report uses medians:**
- Median = typical day (50th percentile, robust to outliers)
- Mean = average (skewed by extreme days)
- Example: Days with 10, 20, 30, 40, 1000 cards → mean=220 (misleading), median=30 (realistic)

This is documented in `docs/anki_data_legend.md` under "MEDIAN VS MEAN ANALYSIS."

## Dependencies

Core stack (see `requirements.txt`):
- `pandas>=2.0.0` - Data manipulation
- `plotly>=5.0.0` - Interactive dashboards
- `matplotlib>=3.5.0` - Static plots
- `reportlab>=4.0.0` - PDF generation
- `numpy>=1.24.0` - Numerical operations

No testing framework or linting is configured for this project.

## Git Workflow Notes

When committing changes:
- User prefers commit messages **without** Claude Code attribution
- Use concise, descriptive commit messages in English
- Focus on the "what" and "why" in bullet points
