#!/usr/bin/env python3
"""
Anki Study Analytics Dashboard Generator

Creates an interactive HTML dashboard from daily review data.
Usage: python3 create_dashboard.py
"""

import os
import sys
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Add dashboard module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dashboard'))

# Import project modules
from config import *
from data_loader import (
    load_anki_data,
    calculate_summary_stats,
    calculate_monthly_stats,
    calculate_weekday_stats,
    find_gaps,
    prepare_heatmap_data
)
from chart_builders import (
    create_key_metrics,
    create_heatmap_calendar,
    create_monthly_time_series,
    create_relearn_rate_chart,
    create_distribution_histogram,
    create_box_plots_by_type,
    create_box_plots_by_weekday,
    create_pie_chart,
    create_cumulative_chart,
    create_streak_visualization,
    create_gap_visualization
)


def create_subplot_structure():
    """
    Create the subplot structure for the dashboard

    Returns:
        plotly.graph_objects.Figure
    """
    fig = make_subplots(
        rows=9, cols=1,
        row_heights=ROW_HEIGHTS[:9],  # Only use first 9 row heights
        specs=[
            [{"type": "indicator"}],    # 1. Key metrics
            [{"type": "heatmap"}],       # 2. Calendar heatmap
            [{"type": "scatter"}],       # 3. Monthly time series
            [{"type": "scatter"}],       # 4. Relearn rate
            [{"type": "histogram"}],     # 5. Distribution
            [{"type": "box"}],           # 6. Box plots by type
            [{"type": "box"}],           # 7. Box plots by weekday
            [{"type": "pie"}],           # 8. Pie chart
            [{"type": "scatter"}],       # 9. Cumulative
        ],
        subplot_titles=(
            "📊 Key Metrics",
            "🗓️ Daily Activity Calendar (GitHub-style)",
            "📈 Study Volume Over Time (Monthly Aggregation)",
            "⚠️ Failure Rate Over Time (Relearn %)",
            "📊 Daily Volume Distribution (Active Days Only)",
            "📦 Performance by Card Type",
            "📅 Performance by Day of Week",
            "🥧 Card Type Breakdown",
            "📈 Cumulative Progress"
        ),
        vertical_spacing=VERTICAL_SPACING
    )

    return fig


def add_all_charts(fig, df, stats, monthly_df, gaps):
    """
    Add all chart traces to the figure

    Args:
        fig: Plotly figure object
        df: Main dataframe
        stats: Summary statistics dict
        monthly_df: Monthly aggregated dataframe
        gaps: List of gap dictionaries
    """
    print("  Adding key metrics...")
    # 1. Key Metrics
    for trace in create_key_metrics(stats):
        fig.add_trace(trace, row=1, col=1)

    print("  Adding heatmap calendar...")
    # 2. Heatmap Calendar
    z_data, x_labels, y_labels = prepare_heatmap_data(df)
    fig.add_trace(create_heatmap_calendar(z_data, x_labels, y_labels), row=2, col=1)

    print("  Adding monthly time series...")
    # 3. Monthly Time Series
    for trace in create_monthly_time_series(monthly_df):
        fig.add_trace(trace, row=3, col=1)

    print("  Adding relearn rate chart...")
    # 4. Relearn Rate
    fig.add_trace(create_relearn_rate_chart(monthly_df), row=4, col=1)

    print("  Adding distribution histogram...")
    # 5. Distribution Histogram
    fig.add_trace(create_distribution_histogram(df), row=5, col=1)

    print("  Adding box plots...")
    # 6. Box Plots by Type
    for trace in create_box_plots_by_type(df):
        fig.add_trace(trace, row=6, col=1)

    # 7. Box Plots by Weekday
    for trace in create_box_plots_by_weekday(df):
        fig.add_trace(trace, row=7, col=1)

    print("  Adding pie chart...")
    # 8. Pie Chart
    fig.add_trace(create_pie_chart(stats), row=8, col=1)

    print("  Adding cumulative chart...")
    # 9. Cumulative Progress
    for trace in create_cumulative_chart(df):
        fig.add_trace(trace, row=9, col=1)

    # Add milestone annotations
    for milestone in CUMULATIVE_MILESTONES:
        milestone_rows = df[df['Cumulative_Total'] >= milestone]
        if not milestone_rows.empty:
            milestone_date = milestone_rows.iloc[0]['Date']
            fig.add_annotation(
                x=milestone_date,
                y=milestone,
                text=f"{milestone:,}",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                row=9, col=1
            )

    # Temporarily disabled - causing overlap issues
    # print("  Adding streak visualization...")
    # # 10. Streaks
    # for trace in create_streak_visualization(df):
    #     fig.add_trace(trace, row=10, col=1)

    return fig


def configure_layout(fig, stats):
    """
    Configure the overall layout and styling

    Args:
        fig: Plotly figure object
        stats: Summary statistics dict
    """
    fig.update_layout(
        title={
            'text': f'{DASHBOARD_TITLE}<br><sub>{stats["date_range"]}</sub>',
            'font': {'size': FONT_SIZES['title'], 'family': FONT_FAMILY},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=DASHBOARD_HEIGHT,
        width=None,  # Let it auto-size to browser width
        autosize=True,  # Enable responsive sizing
        font=dict(
            family=FONT_FAMILY,
            size=FONT_SIZES['body'],
            color=COLORS['text']
        ),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['paper'],
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=COLORS['grid'],
            borderwidth=1
        ),
        margin=MARGINS,
        hovermode='closest'
    )

    # Update x-axes for time series (add range selector)
    fig.update_xaxes(
        rangeselector=dict(
            buttons=TIME_SERIES_RANGE_BUTTONS,
            bgcolor=COLORS['background'],
            activecolor=COLORS['grid']
        ),
        row=3, col=1
    )

    # Update all x-axes
    fig.update_xaxes(
        showgrid=True,
        gridcolor=COLORS['grid'],
        showline=True,
        linecolor=COLORS['grid']
    )

    # Update all y-axes
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLORS['grid'],
        showline=True,
        linecolor=COLORS['grid']
    )

    # Note: Mean line for histogram would be added here but requires calculating actual mean first
    # This can be done by adding a vertical line annotation directly to the histogram data

    return fig


def main():
    """Main execution function"""
    print("=" * 60)
    print("Anki Study Analytics Dashboard Generator")
    print("=" * 60)

    # Check if input file exists
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Error: Input file not found: {INPUT_CSV}")
        print("   Please ensure anki_daily_reviews_honest.csv exists.")
        sys.exit(1)

    # Load data
    print("\n📂 Loading data...")
    df = load_anki_data()
    print(f"   Loaded {len(df)} days of data")

    # Calculate statistics
    print("\n📊 Calculating statistics...")
    stats = calculate_summary_stats(df)
    monthly_df = calculate_monthly_stats(df)
    weekday_df = calculate_weekday_stats(df)
    gaps = find_gaps(df, min_gap_days=STREAK_GAP_THRESHOLD)

    print(f"   Total cards: {stats['total_cards']:,}")
    print(f"   Active days: {stats['active_days']} ({stats['active_days_pct']:.1f}%)")
    print(f"   Longest streak: {stats['max_streak']} days")
    print(f"   Found {len(gaps)} gaps (≥{STREAK_GAP_THRESHOLD} days)")

    # Create dashboard
    print("\n🎨 Building dashboard...")
    fig = create_subplot_structure()

    # Add all charts
    fig = add_all_charts(fig, df, stats, monthly_df, gaps)

    # Configure layout
    print("  Configuring layout...")
    fig = configure_layout(fig, stats)

    # Save to HTML
    print(f"\n💾 Saving dashboard to {OUTPUT_FILE}...")
    fig.write_html(
        OUTPUT_FILE,
        include_plotlyjs=INCLUDE_PLOTLYJS,
        config=PLOTLY_CONFIG
    )

    file_size = os.path.getsize(OUTPUT_FILE) / 1024 / 1024  # MB
    print(f"   File size: {file_size:.2f} MB")

    print("\n✅ Dashboard created successfully!")
    print(f"   Open in browser: file://{OUTPUT_FILE}")
    print("\n" + "=" * 60)

    # Optionally open in browser
    import webbrowser
    webbrowser.open(f'file://{OUTPUT_FILE}')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
