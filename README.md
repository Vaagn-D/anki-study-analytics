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
| **Relearn** | Failed cards | Cards failed on Review, being re-studied | 🔴 Red |
| **Cheated** | Rapid clicking | Cards answered in <1 second (cheating indicator) | ⚪ Removed |
| **Total** | Honest work | Learning + Review - Cheated (real work only) | ⚫ Gray |

### Why "Honest Metrics"?

**Problem 1: Relearn inflates numbers**
1. You review a card (counted once)
2. You fail it and relearn it (counted again)
3. Same card = 2 counts = inflated numbers

**Problem 2: Rapid clicking (cheating)**
1. Answering cards in <1 second = physically impossible to read and think
2. Includes days with 90%+ rapid clicking (obvious cheating)
3. Inflates daily numbers without actual studying

**Solution:**
- `Total = Learning + Review - Cheated` (actual honest work)
- `Relearn` = separate difficulty/persistence indicator
- `Cheated` = quality indicator (removed from Total)

**Example:**
- **Raw:** 176 Review + 13 Relearn + 1 Cheated = 190
- **Honest:** 175 Total + 13 Relearn (separate) + 1 Cheated (removed)

**Validation:** 95% of cheated cards come from 43 "dirty days" (8.2% of active days), with only 0.6 cards/day false positives on clean days.

### Quality Metrics

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Cheated** | Cards answered in <1 second | 0 = honest day ✅, <5% of (L+R) = acceptable ⚠️, >20% = cheating 🚫 |
| **Total** | Learning + Review - Cheated | Honest work metric (excludes Relearn and Cheated) |

**Why track cheating?**
- Identifies days with rapid clicking vs. actual studying
- <1 second threshold is **physically impossible** for genuine study
- Cheated column is the **key quality indicator**
- Already subtracted from Total for honest statistics

**How cheating is measured:**
- Time from showing card front → to pressing answer button
- Threshold: <1000ms (1 second)
- Includes reading question, thinking, showing answer, and clicking button
- Values <1 second = impossible for genuine cognitive processing

**Validation results:**
- 95% of cheated cards come from 43 "dirty days" (8.2% of active days)
- False positive rate: ~0.6 cards/day on clean days
- Total honest work: 36,277 cards (vs. 46,409 raw)

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
- **Total Cards (honest):** 36,277
  - Learning: 10,997 cards (30.3%)
  - Review: 35,412 cards (97.6%)
  - Cheated (removed): 10,132 cards (21.8% of raw total)
- **Relearn:** 5,832 cards (separate difficulty metric)
- **Active Days:** 526 (60.3%)
- **Longest Streak:** 51 days
- **Average:** 41.6 cards/day (all days) | 69.4 cards/day (active days)

### Data Quality
- **Clean days (≤5% cheating):** 455 days (86.5%)
- **Medium days (5-20% cheating):** 28 days (5.3%)
- **Dirty days (>20% cheating):** 43 days (8.2%)
- **Cheated cards breakdown:**
  - From dirty days: 9,624 cards (95.1%)
  - From clean days: 254 cards (2.5%)
  - False positive rate: ~0.6 cards/day on clean days

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
- **Cheating threshold:** Reviews <1000ms flagged as "Cheated" and subtracted from Total

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
