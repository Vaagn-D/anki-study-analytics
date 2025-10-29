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

- Time series trends in Total (work volume over time)
- Relearn rate (%) as difficulty indicator
- Gap analysis (inactive periods)
- Day of week patterns
- Moving averages to identify "rough periods"
- Correlation between Total volume and Relearn rate

---

**Data Integrity:** ✓ Verified against official Anki add-on statistics
**Last Updated:** October 29, 2025
