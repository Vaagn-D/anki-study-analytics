# Anki Study Analytics 📚

Comprehensive analysis pipeline for Anki spaced repetition review data. Extract, process, and visualize your study patterns with interactive dashboards and static plots.

**Period Covered:** June 11, 2023 - October 29, 2025

---

## 📁 Project Structure

```
anki-study-analytics/
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
│
├── data/                        # CSV data files
│   ├── anki_daily_reviews.csv           # Original data + time metrics
│   └── anki_daily_reviews_honest.csv    # Honest metrics (Total = L+R) + time
│
├── scripts/                     # Data processing scripts
│   ├── export_anki_reviews.py           # 1️⃣ Extract from collection.anki2
│   ├── reorganize_csv.py                # 2️⃣ Reorganize with honest metrics
│   ├── plot_anki_data.py                # 3️⃣ Create matplotlib plot
│   ├── create_dashboard.py              # 4️⃣ Dashboard (scrolling version)
│   └── create_dashboard_tabs.py         # 4️⃣ Dashboard with tabs ⭐ (recommended)
│
├── dashboard/                   # Dashboard modules
│   ├── config.py                        # Settings and constants
│   ├── data_loader.py                   # Data loading functions
│   └── chart_builders.py                # Chart creation functions
│
├── output/                      # Generated files
│   ├── anki_dashboard.html              # Interactive dashboard
│   └── anki_review_plot.png             # Static monthly plot
│
└── docs/                        # Documentation
    └── data_legend.md                   # Data legend for statisticians
```

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vaagndanielian/anki-study-analytics.git
   cd anki-study-analytics
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

### Create Dashboard (Recommended)

```bash
cd scripts
python3 create_dashboard_tabs.py
```

The dashboard will automatically open in your browser!

---

## 📊 Complete Workflow

### Step 1: Extract Data from Anki

1. Locate your Anki database:
   - **macOS:** `~/Library/Application Support/Anki2/[Profile]/collection.anki2`
   - **Windows:** `%APPDATA%\Anki2\[Profile]\collection.anki2`
   - **Linux:** `~/.local/share/Anki2/[Profile]/collection.anki2`

2. Copy to Desktop:
   ```bash
   cp ~/Library/Application\ Support/Anki2/User\ 1/collection.anki2 ~/Desktop/
   ```

3. Extract data:
   ```bash
   cd scripts
   python3 export_anki_reviews.py
   ```

**Output:** `data/anki_daily_reviews.csv`

---

### Step 2: Create Honest Metrics

```bash
python3 reorganize_csv.py
```

**What it does:**
- Recalculates `Total = Learning + Review` (excludes Relearn)
- Moves Relearn to last column as separate metric
- Creates: `data/anki_daily_reviews_honest.csv`

**Why?**
- Relearn represents re-studying failed cards
- Including it inflates daily numbers ("sugar coating")
- Total shows real work, Relearn shows difficulty/persistence

---

### Step 3: Create Visualizations

#### Option A: Interactive Dashboard with Tabs ⭐ (Recommended)

```bash
python3 create_dashboard_tabs.py
```

**Features:**
- ✅ 3 organized tabs (Overview, Analysis, Progress)
- ✅ No overlapping charts
- ✅ Modern Bootstrap 5 design
- ✅ Responsive layout

**Output:** `output/anki_dashboard.html` (~130 KB with CDN)

---

#### Option B: Static Matplotlib Plot

```bash
python3 plot_anki_data.py
```

**Features:**
- 4 lines: Learning, Review, Total, Relearn
- Monthly aggregation
- Interactive window (zoom, pan, save)
- High resolution (300 DPI)

**Output:** `output/anki_review_plot.png`

---

## 🎨 Interactive Dashboard

### Dashboard Tabs

**📊 Overview Tab**
- Key metrics (Total Cards, Active Days, Avg/Day, Failure Rate)
- GitHub-style heatmap calendar
- Monthly time series (4 lines)

**🔍 Analysis Tab**
- Relearn rate over time
- Daily volume distribution histogram
- Box plots by card type
- Box plots by day of week
- Pie chart (card type breakdown)

**📈 Progress Tab**
- Cumulative progress chart
- Activity streaks and gaps

---

### Interactivity Features

- 🔍 **Hover tooltips** - See exact values
- 🖱️ **Zoom & Pan** - Mouse wheel to zoom
- 📅 **Range selector** - Filter by date range
- 💾 **Export** - Save as PNG from browser
- 👁️ **Toggle traces** - Click legend to show/hide

---

### Customization

Edit `dashboard/config.py`:

```python
# Change colors
COLORS = {
    'learning': '#2196F3',  # Blue
    'review': '#4CAF50',    # Green
    'total': '#607D8B',     # Gray
    'relearn': '#F44336',   # Red
}

# Change dashboard height
DASHBOARD_HEIGHT = 6000  # pixels

# Change font sizes
FONT_SIZES = {
    'title': 28,
    'body': 12,
}
```

Then regenerate:
```bash
python3 create_dashboard_tabs.py
```

---

## 📖 Understanding the Metrics

### Card Types

| Type | Name | Description | Color |
|------|------|-------------|-------|
| **Learning** | New cards | First-time study of new flashcards | 🔵 Blue |
| **Review** | Graduated cards | Cards with spaced intervals (1d, 1w, 1m, etc.) | 🟢 Green |
| **Total** | Honest work | Learning + Review only (no Relearn) | ⚫ Gray |
| **Relearn** | Failed cards | Cards failed on Review, being re-studied | 🔴 Red |

### Why "Honest Metrics"?

**Problem:** Including Relearn in Total inflates numbers because:
1. You review a card (counted once)
2. You fail it and relearn it (counted again)
3. Same card = 2 counts = inflated numbers

**Solution:**
- `Total = Learning + Review` (actual unique work)
- `Relearn` = separate difficulty/persistence indicator

**Example:**
- **Inflated:** 176 Review + 13 Relearn = 189 Total
- **Honest:** 176 Total + 13 Relearn (shown separately)

**Relearn Rate** = Relearn / Total × 100 = difficulty indicator

### Time & Quality Metrics

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **AvgTime** | Average seconds per card | 20-40s = normal pace, <5s = rushing/cheating, >60s = difficult cards |
| **MedianTime** | Middle value of review times | More stable than average, not affected by outliers |
| **FastCount** | Reviews completed in <1 second | 0-10 = acceptable, >20% of total = suspicious |
| **FastPercent** | Percentage of fast reviews | **<5%** = honest ✅, **5-10%** = rushing ⚠️, **>20%** = cheating 🚫 |

**Why track time?**
- Identifies days with rapid clicking (cheating) vs. actual studying
- FastPercent is the **key quality indicator**
- Allows filtering for honest-only statistics
- Example: 430 cards at 0.4s average = 98% fast reviews = obvious cheating

**How time is measured:**
- From showing card front → to pressing answer button
- Includes time to read question, show answer, and click button
- Values <1 second are physically impossible for genuine study

---

## 🔄 Updating the Analysis

When you have new Anki data:

```bash
# 1. Copy fresh database
cp ~/Library/Application\ Support/Anki2/User\ 1/collection.anki2 ~/Desktop/

# 2. Run the pipeline
cd scripts
python3 export_anki_reviews.py
python3 reorganize_csv.py
python3 create_dashboard_tabs.py

# 3. Commit changes (optional)
git add ../data/ ../output/
git commit -m "Update: data through $(date +%Y-%m-%d)"
git push
```

---

## 📤 Sharing the Dashboard

### Option 1: With Internet (CDN)

Default configuration uses CDN:
- File size: ~130 KB
- Requires internet to view
- Best for sharing via web

### Option 2: Offline (Embedded JS)

Edit `dashboard/config.py`:
```python
INCLUDE_PLOTLYJS = True  # Was: 'cdn'
```

Regenerate:
```bash
python3 create_dashboard_tabs.py
```

Result:
- File size: ~3.5 MB
- Works offline
- Best for local use or email

---

## 🆘 Troubleshooting

**Dashboard not loading?**
- Check internet connection (if using CDN)
- Or switch to embedded JS (see above)

**Charts overlapping?**
- Use tabbed version: `python3 create_dashboard_tabs.py`
- Or increase `DASHBOARD_HEIGHT` in `dashboard/config.py`

**Import errors in scripts?**
- Ensure you run scripts from `scripts/` directory
- Or use: `python3 scripts/create_dashboard_tabs.py` from root

**Pandas FutureWarning?**
- This is just a warning, not an error
- Dashboard will still generate correctly

**Database locked error?**
- Close Anki completely
- Wait 10 seconds
- Try again

---

## 📊 Statistics

### Volume & Activity
- **Period:** June 11, 2023 - October 29, 2025 (872 days)
- **Total Cards (honest):** 46,409
  - Learning: 10,997 cards (23.7%)
  - Review: 35,412 cards (76.3%)
- **Relearn:** 5,832 cards (12.6% failure rate)
- **Active Days:** 526 (60.3%)
- **Longest Streak:** 51 days
- **Average:** 53.2 cards/day (all days) | 88.2 cards/day (active days)

### Time & Quality Metrics
- **Average time per card:** 40.3 seconds
- **Median time per card:** 19.1 seconds
- **Average fast review rate:** 6.54%
- **Honest study days (<10% fast):** 501 days (95.2%)
- **Days with suspected cheating (>20% fast):** 25 days (4.8%)
- **Estimated cheating cards:** ~10,000+ cards across suspicious days

---

## 🛠️ Technical Details

### Dependencies

- **pandas** - Data manipulation
- **plotly** - Interactive charts
- **matplotlib** - Static plots
- **numpy** - Numerical operations

### Data Source

Anki stores review history in SQLite database (`collection.anki2`):
- **Table:** `revlog`
- **Columns extracted:**
  - `id` - Timestamp (milliseconds since epoch)
  - `type` - Card type: 0 (Learning), 1 (Review), 2 (Relearn)
  - `time` - Review duration in milliseconds (front display → answer button)
- **Excluded types:** 3 (Filtered/Cram), 4 (Manual/Unknown)
- **Timezone:** Moscow Time (MSK, UTC+3) via localtime conversion
- **Quality threshold:** Reviews <1000ms flagged as "fast" (possible cheating)

### Chart Types

Dashboard includes 9 chart types:
1. **Indicator cards** - Key metrics
2. **Heatmap** - GitHub-style calendar
3. **Line chart** - Monthly time series
4. **Area chart** - Relearn rate
5. **Histogram** - Distribution
6. **Box plots** - By card type and weekday
7. **Pie chart** - Card type breakdown
8. **Line chart** - Cumulative progress
9. **Bar chart** - Activity streaks

---

## 📝 License

This project is provided as-is for personal use. Feel free to fork and modify!

---

## 🤝 Contributing

For issues or suggestions, please open an issue on GitHub.

---

**Last Updated:** October 29, 2025
**Repository:** https://github.com/vaagndanielian/anki-study-analytics

---

## 🎯 Quick Commands Reference

```bash
# Full pipeline
cd scripts
python3 export_anki_reviews.py && python3 reorganize_csv.py && python3 create_dashboard_tabs.py

# Just update dashboard
python3 create_dashboard_tabs.py

# Create static plot
python3 plot_anki_data.py

# View dashboard
open ../output/anki_dashboard.html  # macOS
xdg-open ../output/anki_dashboard.html  # Linux
start ../output/anki_dashboard.html  # Windows
```

---

Happy studying! 📚✨
