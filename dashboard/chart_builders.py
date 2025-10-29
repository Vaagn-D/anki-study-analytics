"""
Chart building functions for Anki Dashboard
Each function returns traces that can be added to a figure
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from config import COLORS, HEATMAP_COLORBAR_TITLE, CUMULATIVE_MILESTONES


def create_key_metrics(stats):
    """
    Create key metrics indicators

    Args:
        stats: Dictionary from calculate_summary_stats()

    Returns:
        list: List of Indicator traces
    """
    traces = []

    # Total Cards Studied
    traces.append(go.Indicator(
        mode="number",
        value=stats['total_cards'],
        title={"text": "Total Cards<br>Studied", "font": {"size": 14}},
        number={'valueformat': ',', 'font': {'size': 32, 'color': COLORS['total']}},
        domain={'x': [0, 0.25], 'y': [0, 1]}
    ))

    # Average per Day
    traces.append(go.Indicator(
        mode="number",
        value=stats['avg_per_day'],
        title={"text": "Avg Cards/Day<br>(All Days)", "font": {"size": 14}},
        number={'suffix': " cards", 'valueformat': '.1f', 'font': {'size': 32, 'color': COLORS['learning']}},
        domain={'x': [0.25, 0.5], 'y': [0, 1]}
    ))

    # Active Days Percentage (Gauge)
    traces.append(go.Indicator(
        mode="gauge+number",
        value=stats['active_days_pct'],
        title={"text": f"Active Days<br>{stats['active_days']}/{stats['total_days']}", "font": {"size": 14}},
        gauge={
            'axis': {'range': [0, 100], 'ticksuffix': '%'},
            'bar': {'color': COLORS['review']},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': COLORS['grid'],
            'steps': [
                {'range': [0, 33], 'color': '#FFCDD2'},
                {'range': [33, 66], 'color': '#FFF9C4'},
                {'range': [66, 100], 'color': '#C8E6C9'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        },
        number={'suffix': "%", 'valueformat': '.1f', 'font': {'size': 32}},
        domain={'x': [0.5, 0.75], 'y': [0, 1]}
    ))

    # Relearn Rate (Failure Rate)
    traces.append(go.Indicator(
        mode="number",
        value=stats['relearn_rate'],
        title={"text": "Failure Rate<br>(Relearn %)", "font": {"size": 14}},
        number={'suffix': "%", 'valueformat': '.1f', 'font': {'size': 32, 'color': COLORS['relearn']}},
        domain={'x': [0.75, 1], 'y': [0, 1]}
    ))

    return traces


def create_heatmap_calendar(z_data, x_labels, y_labels):
    """
    Create GitHub-style heatmap calendar

    Args:
        z_data: 2D array (weekdays x weeks)
        x_labels: Week labels
        y_labels: Day labels

    Returns:
        go.Heatmap trace
    """
    trace = go.Heatmap(
        z=z_data,
        x=x_labels,
        y=y_labels,
        colorscale=COLORS['heatmap'],
        showscale=True,
        colorbar=dict(
            title=dict(text=HEATMAP_COLORBAR_TITLE, side='right'),
            tickmode='linear',
            tick0=0,
            dtick=50
        ),
        hovertemplate='<b>%{x}</b><br>%{y}<br>Cards: %{z}<extra></extra>',
        xgap=3,
        ygap=3
    )

    return trace


def create_monthly_time_series(monthly_df):
    """
    Create monthly time series with 4 lines (like matplotlib plot)

    Args:
        monthly_df: DataFrame with Monthly, Learning, Review, Relearn, Total columns

    Returns:
        list: List of Scatter traces
    """
    traces = []

    # Convert Month strings to dates for plotting
    monthly_df['MonthDate'] = pd.to_datetime(monthly_df['Month'] + '-01')

    # Learning (Blue)
    traces.append(go.Scatter(
        x=monthly_df['MonthDate'],
        y=monthly_df['Learning'],
        name='Learning (New Cards)',
        mode='lines+markers',
        line=dict(color=COLORS['learning'], width=2),
        marker=dict(size=6, symbol='circle'),
        hovertemplate='<b>%{x|%b %Y}</b><br>Learning: %{y:,}<extra></extra>'
    ))

    # Review (Green)
    traces.append(go.Scatter(
        x=monthly_df['MonthDate'],
        y=monthly_df['Review'],
        name='Review',
        mode='lines+markers',
        line=dict(color=COLORS['review'], width=2),
        marker=dict(size=6, symbol='square'),
        hovertemplate='<b>%{x|%b %Y}</b><br>Review: %{y:,}<extra></extra>'
    ))

    # Total (Gray, thicker)
    traces.append(go.Scatter(
        x=monthly_df['MonthDate'],
        y=monthly_df['Total'],
        name='Total (Learning + Review)',
        mode='lines+markers',
        line=dict(color=COLORS['total'], width=3),
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='<b>%{x|%b %Y}</b><br>Total: %{y:,}<extra></extra>'
    ))

    # Relearn (Red)
    traces.append(go.Scatter(
        x=monthly_df['MonthDate'],
        y=monthly_df['Relearn'],
        name='Relearn (Failed Cards)',
        mode='lines+markers',
        line=dict(color=COLORS['relearn'], width=2),
        marker=dict(size=6, symbol='triangle-up'),
        hovertemplate='<b>%{x|%b %Y}</b><br>Relearn: %{y:,}<extra></extra>'
    ))

    return traces


def create_relearn_rate_chart(monthly_df):
    """
    Create Relearn Rate % over time

    Args:
        monthly_df: DataFrame with Month and RelearnRate columns

    Returns:
        go.Scatter trace
    """
    monthly_df['MonthDate'] = pd.to_datetime(monthly_df['Month'] + '-01')

    trace = go.Scatter(
        x=monthly_df['MonthDate'],
        y=monthly_df['RelearnRate'],
        name='Relearn Rate %',
        mode='lines+markers',
        line=dict(color=COLORS['relearn'], width=2),
        fill='tozeroy',
        fillcolor=f"rgba(244, 67, 54, 0.2)",
        marker=dict(size=6),
        hovertemplate='<b>%{x|%b %Y}</b><br>Failure Rate: %{y:.1f}%<extra></extra>'
    )

    return trace


def create_distribution_histogram(df):
    """
    Create distribution histogram of daily study volume

    Args:
        df: DataFrame with Total column

    Returns:
        go.Histogram trace
    """
    # Only active days
    active_days = df[df['IsActive']]['Total']

    trace = go.Histogram(
        x=active_days,
        nbinsx=30,
        marker=dict(
            color=COLORS['ma7'],
            line=dict(color='white', width=1)
        ),
        hovertemplate='Cards: %{x}<br>Days: %{y}<extra></extra>',
        showlegend=False,
        name='Distribution'
    )

    return trace


def create_box_plots_by_type(df):
    """
    Create box plots by card type

    Args:
        df: DataFrame with Learning, Review, Relearn columns

    Returns:
        list: List of Box traces
    """
    traces = []

    # Filter out zeros for better visualization
    learning_data = df[df['Learning'] > 0]['Learning']
    review_data = df[df['Review'] > 0]['Review']
    relearn_data = df[df['Relearn'] > 0]['Relearn']

    traces.append(go.Box(
        y=learning_data,
        name='Learning',
        marker_color=COLORS['learning'],
        boxmean='sd',  # Show mean and standard deviation
        hovertemplate='Learning<br>Value: %{y}<extra></extra>'
    ))

    traces.append(go.Box(
        y=review_data,
        name='Review',
        marker_color=COLORS['review'],
        boxmean='sd',
        hovertemplate='Review<br>Value: %{y}<extra></extra>'
    ))

    traces.append(go.Box(
        y=relearn_data,
        name='Relearn',
        marker_color=COLORS['relearn'],
        boxmean='sd',
        hovertemplate='Relearn<br>Value: %{y}<extra></extra>'
    ))

    return traces


def create_box_plots_by_weekday(df):
    """
    Create box plots by day of week

    Args:
        df: DataFrame with DayOfWeek and Total columns

    Returns:
        list: List of Box traces
    """
    traces = []

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_colors = ['#1976D2', '#1976D2', '#1976D2', '#1976D2', '#1976D2', '#FF9800', '#F44336']

    for day, color in zip(days_order, day_colors):
        day_data = df[df['DayOfWeek'] == day]['Total']

        traces.append(go.Box(
            y=day_data,
            name=day[:3],  # Mon, Tue, etc.
            marker_color=color,
            boxmean=True,
            hovertemplate=f'<b>{day}</b><br>Cards: %{{y}}<extra></extra>'
        ))

    return traces


def create_pie_chart(stats):
    """
    Create pie/donut chart for card type breakdown

    Args:
        stats: Dictionary from calculate_summary_stats()

    Returns:
        go.Pie trace
    """
    labels = ['Learning', 'Review', 'Relearn']
    values = [stats['total_learning'], stats['total_review'], stats['total_relearn']]
    colors_list = [COLORS['learning'], COLORS['review'], COLORS['relearn']]

    trace = go.Pie(
        labels=labels,
        values=values,
        hole=0.4,  # Donut chart
        marker=dict(colors=colors_list, line=dict(color='white', width=2)),
        textposition='auto',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Cards: %{value:,}<br>Percent: %{percent}<extra></extra>'
    )

    return trace


def create_cumulative_chart(df):
    """
    Create cumulative progress chart

    Args:
        df: DataFrame with Date and Cumulative_Total columns

    Returns:
        list: List of traces (Scatter + annotations)
    """
    traces = []

    # Main cumulative line
    traces.append(go.Scatter(
        x=df['Date'],
        y=df['Cumulative_Total'],
        name='Cumulative Cards',
        mode='lines',
        line=dict(color=COLORS['ma30'], width=2),
        fill='tozeroy',
        fillcolor=f"rgba(156, 39, 176, 0.2)",
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>Total: %{y:,} cards<extra></extra>'
    ))

    return traces


def create_streak_visualization(df):
    """
    Create streak analysis visualization

    Args:
        df: DataFrame with Date, Streak, IsActive columns

    Returns:
        list: List of traces
    """
    traces = []

    # Bar chart showing streak length over time
    streak_colors = [COLORS['streak_active'] if active else COLORS['streak_inactive']
                     for active in df['IsActive']]

    traces.append(go.Bar(
        x=df['Date'],
        y=df['IsActive'].astype(int),  # 1 for active, 0 for inactive
        marker=dict(color=streak_colors, line=dict(width=0)),
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>%{customdata}<extra></extra>',
        customdata=['Active' if a else 'Inactive' for a in df['IsActive']],
        showlegend=False
    ))

    return traces


def create_gap_visualization(gaps):
    """
    Create gap visualization

    Args:
        gaps: List of dictionaries from find_gaps()

    Returns:
        list: List of traces
    """
    traces = []

    if not gaps:
        # No gaps found
        traces.append(go.Scatter(
            x=[],
            y=[],
            mode='markers',
            name='No gaps found',
            showlegend=False
        ))
        return traces

    # Create bar chart of gaps
    gap_starts = [g['start'] for g in gaps]
    gap_lengths = [g['length'] for g in gaps]
    gap_colors = [COLORS['gap_long'] if length > 14 else COLORS['gap_short'] for length in gap_lengths]

    traces.append(go.Bar(
        x=gap_starts,
        y=gap_lengths,
        marker=dict(color=gap_colors, line=dict(color='white', width=1)),
        hovertemplate='<b>Gap Start:</b> %{x|%b %d, %Y}<br><b>Length:</b> %{y} days<extra></extra>',
        showlegend=False,
        name='Gaps'
    ))

    return traces
