"""
Data loading and preprocessing for Anki Dashboard
"""

import pandas as pd
import numpy as np
from config import INPUT_CSV, MIN_CARDS_FOR_ACTIVE_DAY, MOVING_AVERAGES

def load_anki_data():
    """
    Load and preprocess Anki CSV data

    Returns:
        pd.DataFrame: Preprocessed dataframe with additional computed columns
    """
    # Read CSV
    df = pd.read_csv(INPUT_CSV)
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)

    # Add computed columns
    df = _add_time_features(df)
    df = _add_moving_averages(df)
    df = _add_cumulative_metrics(df)
    df = _add_activity_flags(df)
    df = _add_streaks(df)

    return df


def _add_time_features(df):
    """Add time-related features"""
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['DayOfWeekNum'] = df['Date'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['Month'] = df['Date'].dt.to_period('M')
    df['MonthStr'] = df['Date'].dt.strftime('%Y-%m')
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Year'] = df['Date'].dt.year
    df['YearWeek'] = df['Year'].astype(str) + '-W' + df['Week'].astype(str).str.zfill(2)
    df['DayOfYear'] = df['Date'].dt.dayofyear

    return df


def _add_moving_averages(df):
    """Add moving averages for Total"""
    for window in MOVING_AVERAGES:
        df[f'Total_MA{window}'] = df['Total'].rolling(window=window, center=True).mean()

    return df


def _add_cumulative_metrics(df):
    """Add cumulative sums"""
    df['Cumulative_Total'] = df['Total'].cumsum()
    df['Cumulative_Learning'] = df['Learning'].cumsum()
    df['Cumulative_Review'] = df['Review'].cumsum()
    df['Cumulative_Relearn'] = df['Relearn'].cumsum()

    return df


def _add_activity_flags(df):
    """Add boolean flags for activity"""
    df['IsActive'] = df['Total'] >= MIN_CARDS_FOR_ACTIVE_DAY
    df['IsZero'] = df['Total'] == 0

    return df


def _add_streaks(df):
    """
    Add streak information
    - Streak = consecutive days with activity
    """
    df['Streak'] = 0
    current_streak = 0

    for idx, row in df.iterrows():
        if row['IsActive']:
            current_streak += 1
            df.at[idx, 'Streak'] = current_streak
        else:
            current_streak = 0
            df.at[idx, 'Streak'] = 0

    return df


def calculate_summary_stats(df):
    """
    Calculate summary statistics

    Returns:
        dict: Dictionary with key metrics
    """
    total_cards = int(df['Total'].sum())
    total_learning = int(df['Learning'].sum())
    total_review = int(df['Review'].sum())
    total_relearn = int(df['Relearn'].sum())

    total_days = len(df)
    active_days = int(df['IsActive'].sum())
    inactive_days = total_days - active_days

    avg_per_day = total_cards / total_days if total_days > 0 else 0
    avg_per_active_day = total_cards / active_days if active_days > 0 else 0

    relearn_rate = (total_relearn / total_cards * 100) if total_cards > 0 else 0

    # Streaks
    max_streak = int(df['Streak'].max())
    current_streak = int(df.iloc[-1]['Streak']) if len(df) > 0 else 0

    # Learning percentage
    learning_pct = (total_learning / total_cards * 100) if total_cards > 0 else 0
    review_pct = (total_review / total_cards * 100) if total_cards > 0 else 0

    # Active days percentage
    active_days_pct = (active_days / total_days * 100) if total_days > 0 else 0

    return {
        'total_cards': total_cards,
        'total_learning': total_learning,
        'total_review': total_review,
        'total_relearn': total_relearn,

        'total_days': total_days,
        'active_days': active_days,
        'inactive_days': inactive_days,
        'active_days_pct': active_days_pct,

        'avg_per_day': avg_per_day,
        'avg_per_active_day': avg_per_active_day,

        'relearn_rate': relearn_rate,

        'max_streak': max_streak,
        'current_streak': current_streak,

        'learning_pct': learning_pct,
        'review_pct': review_pct,

        'date_range': f"{df['Date'].min().strftime('%B %d, %Y')} - {df['Date'].max().strftime('%B %d, %Y')}",
    }


def calculate_monthly_stats(df):
    """
    Calculate monthly aggregated statistics

    Returns:
        pd.DataFrame: Monthly aggregated data
    """
    monthly = df.groupby('MonthStr').agg({
        'Learning': 'sum',
        'Review': 'sum',
        'Relearn': 'sum',
        'Total': 'sum',
        'IsActive': 'sum'  # Count of active days
    }).reset_index()

    monthly.columns = ['Month', 'Learning', 'Review', 'Relearn', 'Total', 'ActiveDays']

    # Add Relearn rate per month
    monthly['RelearnRate'] = (monthly['Relearn'] / monthly['Total'] * 100).fillna(0)

    return monthly


def calculate_weekday_stats(df):
    """
    Calculate statistics by day of week

    Returns:
        pd.DataFrame: Aggregated by weekday
    """
    # Order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)

    weekday = df.groupby('DayOfWeek').agg({
        'Total': ['mean', 'median', 'std', 'sum'],
        'IsActive': 'sum'
    }).reset_index()

    weekday.columns = ['DayOfWeek', 'Mean', 'Median', 'Std', 'Total', 'ActiveDays']

    return weekday


def find_gaps(df, min_gap_days=3):
    """
    Find periods of inactivity (gaps)

    Args:
        df: DataFrame with Date and IsActive columns
        min_gap_days: Minimum days of inactivity to count as a gap

    Returns:
        list: List of dicts with gap start, end, and length
    """
    gaps = []
    current_gap_start = None
    gap_length = 0

    for idx, row in df.iterrows():
        if not row['IsActive']:
            if current_gap_start is None:
                current_gap_start = row['Date']
            gap_length += 1
        else:
            if current_gap_start is not None and gap_length >= min_gap_days:
                gaps.append({
                    'start': current_gap_start,
                    'end': df.iloc[idx-1]['Date'],
                    'length': gap_length
                })
            current_gap_start = None
            gap_length = 0

    # Handle gap at the end
    if current_gap_start is not None and gap_length >= min_gap_days:
        gaps.append({
            'start': current_gap_start,
            'end': df.iloc[-1]['Date'],
            'length': gap_length
        })

    return gaps


def prepare_heatmap_data(df):
    """
    Prepare data for GitHub-style heatmap calendar

    Returns:
        tuple: (z_data, x_labels, y_labels)
    """
    # Create pivot table: rows=weekday, columns=week
    heatmap_pivot = df.pivot_table(
        values='Total',
        index='DayOfWeekNum',
        columns='YearWeek',
        aggfunc='sum',
        fill_value=0
    )

    # Sort by weekday (Monday=0 to Sunday=6)
    heatmap_pivot = heatmap_pivot.sort_index()

    # Y labels (days of week)
    y_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # X labels (weeks)
    x_labels = heatmap_pivot.columns.tolist()

    # Z data (matrix)
    z_data = heatmap_pivot.values

    return z_data, x_labels, y_labels
