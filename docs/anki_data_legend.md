# ANKI REVIEW DATA - LEGEND & DESCRIPTION

**File:** `anki_daily_reviews_honest.csv`

**Period:** June 11, 2023 to October 29, 2025 (872 days)

**Data Source:** Anki spaced repetition software database (collection.anki2 SQLite revlog table)

---

## COLUMN DEFINITIONS

### Date
Calendar date (YYYY-MM-DD format)

### Learning
Number of new card review events
- First-time exposures to new flashcards
- Type 0 events in revlog

### Review
Number of review events for graduated cards
- Cards with spaced intervals (1 day, 1 week, 1 month, etc.)
- Type 1 events in revlog

### Total
**Primary metric: Learning + Review**
- Represents actual work done without inflation
- Does NOT include Relearn events (see below)
- Use this as the main "cards studied per day" metric

### Relearn
Number of relearning events
- Cards that were failed during Review and required relearning
- Type 2 events in revlog
- **Interpretation:** Indicator of difficulty and persistence
  - Higher Relearn = more challenging period
  - But also shows effort (didn't give up after failures)
- **NOT included in Total** to avoid double-counting

### AvgTime
Average time per card in seconds
- Mean of all review times for the day (from revlog.time column)
- Time measured from card front display to answer button press
- **Interpretation:** Study pace indicator
  - 20-40 seconds = normal pace
  - <5 seconds = likely rushing or cheating
  - >60 seconds = careful study or difficult cards

### MedianTime
Median time per card in seconds
- Middle value of all review times for the day
- More stable than average (not affected by outliers)
- **Use this** when average is skewed by very long/short reviews

### FastCount
Number of "fast" reviews (<1 second)
- Count of cards answered in less than 1000ms
- **Interpretation:** Quality indicator
  - 0-10 fast reviews = acceptable (accidental quick answers)
  - >20% of total = suspicious, possible cheating
  - >90% of total = definite rapid clicking without studying

### FastPercent
Percentage of fast reviews
- `(FastCount / Total) * 100`
- **Key quality metric** for identifying honest vs. dishonest study sessions
- **Thresholds:**
  - <5% = Honest studying ✅
  - 5-10% = Possibly rushing ⚠️
  - 10-20% = Likely some cheating 🚨
  - >20% = Definite cheating 🚫

---

## KEY METRICS

**Total Cards (honest work):** 46,409
- Learning: 10,997
- Review: 35,412

**Relearn (effort on mistakes):** 5,832

**Active Days:** 526 out of 872 days
**Inactive Days (zeros):** 346 days

**Average per day (all days):** 53.2 cards
**Average per active day:** 88.2 cards

**Time Metrics (active days only):**
- Average time per card: 40.3 seconds
- Median time per card: 19.1 seconds
- Average fast review rate: 6.54%

**Data Quality:**
- Days with honest studying (<10% fast): 501 days (95.2%)
- Days with suspected cheating (>20% fast): 25 days (4.8%)
- Cheating cards identified: ~10,000+ cards across 25 days

---

## IMPORTANT NOTES

1. **Events vs. Unique Cards:** Each number represents review *events*, not unique cards. A single card may generate multiple events if reviewed multiple times in one day.

2. **Timezone:** All dates use Moscow Time (MSK, UTC+3) with local system timezone conversion.

3. **Missing Card Types:** Excludes Type 3 (Filtered/Cram deck) and Type 4 events (98 + 81,803 events respectively) as these are not standard reviews.

4. **Zero Days:** Days with all zeros = no studying activity that day.

5. **Relearn Interpretation:**
   - `Relearn / Total` ratio = failure rate (difficulty indicator)
   - Example: 13 Relearn / 176 Total = 7.4% failure rate

---

## SUGGESTED ANALYSES

**Volume & Difficulty:**
- Time series trends in Total (work volume over time)
- Relearn rate (%) as difficulty indicator
- Gap analysis (inactive periods)
- Day of week patterns
- Moving averages to identify "rough periods"
- Correlation between Total volume and Relearn rate

**Study Quality & Pace:**
- FastPercent distribution to identify cheating patterns
- AvgTime vs. MedianTime to detect outliers
- Study pace trends over time (is studying getting faster/slower?)
- Correlation between FastPercent and Relearn rate (rushed studying = more failures?)
- Filter out cheating days (>20% fast) for honest statistics
- Time of day patterns (if timestamp data available)
- Optimal study pace identification (balance speed vs. retention)

**Recommended Filters for Honest Analysis:**
- `FastPercent < 10%` for clean data
- `AvgTime > 5s` to exclude rapid clicking sessions
- Exclude days with >90% FastPercent (obvious cheating)

---

**Data Integrity:** ✓ Verified against official Anki add-on statistics
**Last Updated:** October 29, 2025
