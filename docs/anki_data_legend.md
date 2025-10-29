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

### Relearn
Number of relearning events
- Cards that were failed during Review and required relearning
- Type 2 events in revlog
- **Interpretation:** Indicator of difficulty and persistence
  - Higher Relearn = more challenging period
  - But also shows effort (didn't give up after failures)
- **NOT included in Total** to avoid double-counting

### Cheated
Number of "cheating" reviews (<1 second)
- Count of cards answered in less than 1000ms
- Time measured from card front display to answer button press
- **Interpretation:** Quality/honesty indicator
  - 0 cheated = honest day ✅
  - <5% of (L+R) = acceptable (few accidental quick answers)
  - >20% of (L+R) = suspicious, rapid clicking without studying
  - >90% of (L+R) = definite cheating day
- **Subtracted from Total** to provide honest work metric
- **Analysis:** 95% of cheated cards come from 43 "dirty days" (8.2% of active days)

### Total
**Primary metric: Learning + Review - Cheated**
- Represents actual honest work done
- Does NOT include Relearn events (avoid double-counting)
- Does NOT include Cheated events (avoid counting rapid clicking)
- Use this as the main "honest cards studied per day" metric
- **Formula:** `Total = Learning + Review - Cheated`

---

## KEY METRICS

**Total Cards (honest work):** 36,277
- Learning: 10,997
- Review: 35,412
- Cheated (removed): 10,132

**Relearn (effort on mistakes):** 5,832

**Active Days:** 526 out of 872 days
**Inactive Days (zeros):** 346 days

**Average per day (all days):** 41.6 cards
**Average per active day:** 69.4 cards

**Data Quality:**
- Clean days (≤5% cheating): 455 days (86.5%)
- Medium days (5-20% cheating): 28 days (5.3%)
- Dirty days (>20% cheating): 43 days (8.2%)
- Cheated cards breakdown:
  - From dirty days: 9,624 cards (95.1%)
  - From clean days: 254 cards (2.5%)
  - False positive rate: ~0.6 cards/day on clean days

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
- Time series trends in Total (honest work volume over time)
- Relearn rate (%) as difficulty indicator
- Gap analysis (inactive periods)
- Day of week patterns
- Moving averages to identify "rough periods"
- Correlation between Total volume and Relearn rate

**Study Quality:**
- Cheating rate distribution: `Cheated / (Learning + Review) * 100`
- Identify periods with high cheating (>20%)
- Correlation between Cheated rate and Relearn rate (rushed studying = more failures?)
- Compare clean days vs. dirty days performance

**Honest Statistics:**
- Total already excludes cheated cards (no filtering needed)
- For stricter analysis, exclude days with >20% cheating rate
- Compare metrics before/after cheating removal

---

## MEDIAN VS MEAN ANALYSIS

### Why Use Median?

**Median** represents the "typical day" - the middle value when all active days are sorted:
- **Robust to outliers:** A few very high or very low days don't skew the result
- **Better represents reality:** Shows what a normal study day actually looks like
- **Easier to plan around:** More reliable for setting daily targets

**Mean (Average)** can be misleading for planning:
- **Sensitive to outliers:** A few extreme days can drastically change the average
- **Can overestimate typical performance:** High outliers inflate the average
- **Less useful for benchmarking:** May set unrealistic expectations

### Example

If you have study days with: 10, 20, 30, 40, 1000 cards
- **Mean:** 220 cards/day (misleading - you never study 220 cards normally!)
- **Median:** 30 cards/day (realistic - this is your typical day)

### Professional PDF Report

**File:** `output/march_2025_median_comparison.pdf`

A professional analysis report comparing:
- **Baseline Period:** June 2023 - October 2025 (entire dataset)
- **March 2025:** Best performance month

**Report Sections:**
1. Executive Summary
2. Activity Overview (total days, active days, activity rate)
3. Performance Metrics (median values for typical day)
4. Quality Metrics (cheating analysis and data integrity)
5. Key Findings
6. Benchmark Summary (consolidated reference)

**Use Case:**
- Template for benchmarking against future periods
- Specifically designed for comparing with November 2025 daily work target
- Focus on activity rate (58.1% intermittent vs. 100% daily consistency)

**Key Differences from Dashboard:**
- Uses median instead of mean
- Focuses on typical day rather than monthly aggregates
- Professional business format
- Designed for printing and formal comparison

---

**Data Integrity:** ✓ Verified against official Anki add-on statistics
**Last Updated:** October 29, 2025
