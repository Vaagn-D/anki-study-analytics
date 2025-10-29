#!/usr/bin/env python3
"""
Anki Study Analytics Dashboard Generator - Tabbed Version

Creates an interactive HTML dashboard with tabs from daily review data.
Usage: python3 create_dashboard_tabs.py
"""

import os
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    create_heatmap_calendar,
    create_monthly_time_series,
    create_relearn_rate_chart,
    create_distribution_histogram,
    create_box_plots_by_type,
    create_box_plots_by_weekday,
    create_pie_chart,
    create_cumulative_chart,
    create_streak_visualization
)


def create_overview_tab(df, stats, monthly_df):
    """Create Overview tab with key metrics and main charts"""

    fig = make_subplots(
        rows=3, cols=1,
        row_heights=[0.25, 0.35, 0.40],
        specs=[
            [{"type": "xy"}],      # Key metrics as text/numbers
            [{"type": "heatmap"}],  # Calendar heatmap
            [{"type": "scatter"}],  # Monthly time series
        ],
        subplot_titles=(
            "📊 Key Performance Indicators",
            "🗓️ Daily Activity Calendar (GitHub-style)",
            "📈 Study Volume Over Time (Monthly)"
        ),
        vertical_spacing=0.08
    )

    # 1. Key Metrics - as annotations instead of indicator
    metrics = [
        {"label": "Total Cards", "value": f"{stats['total_cards']:,}", "x": 0.12},
        {"label": "Active Days", "value": f"{stats['active_days']}", "x": 0.37},
        {"label": "Avg/Day", "value": f"{stats['avg_per_day']:.1f}", "x": 0.62},
        {"label": "Failure Rate", "value": f"{stats['relearn_rate']:.1f}%", "x": 0.87},
    ]

    for metric in metrics:
        # Value (big number)
        fig.add_annotation(
            text=metric["value"],
            xref="paper", yref="paper",
            x=metric["x"], y=0.23,
            showarrow=False,
            font=dict(size=36, color=COLORS['total'], family=FONT_FAMILY),
            xanchor="center"
        )
        # Label (small text)
        fig.add_annotation(
            text=metric["label"],
            xref="paper", yref="paper",
            x=metric["x"], y=0.18,
            showarrow=False,
            font=dict(size=12, color=COLORS['text_muted'], family=FONT_FAMILY),
            xanchor="center"
        )

    # 2. Heatmap
    z_data, x_labels, y_labels = prepare_heatmap_data(df)
    fig.add_trace(create_heatmap_calendar(z_data, x_labels, y_labels), row=2, col=1)

    # 3. Monthly Time Series
    for trace in create_monthly_time_series(monthly_df):
        fig.add_trace(trace, row=3, col=1)

    # Update layout
    fig.update_layout(
        height=1200,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=80, r=80, t=100, b=80),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['paper'],
        font=dict(family=FONT_FAMILY, size=12, color=COLORS['text'])
    )

    # Hide x/y axes for metrics row
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, row=1, col=1)

    # Grid for other charts
    fig.update_xaxes(showgrid=True, gridcolor=COLORS['grid'], row=2, col=1)
    fig.update_xaxes(showgrid=True, gridcolor=COLORS['grid'], row=3, col=1)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS['grid'], row=2, col=1)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS['grid'], row=3, col=1)

    return fig


def create_analysis_tab(df, monthly_df, stats):
    """Create Analysis tab with detailed charts"""

    fig = make_subplots(
        rows=3, cols=2,
        specs=[
            [{"type": "scatter"}, {"type": "histogram"}],
            [{"type": "box"}, {"type": "box"}],
            [{"type": "pie", "colspan": 2}, None],
        ],
        subplot_titles=(
            "⚠️ Failure Rate Over Time (Relearn %)",
            "📊 Daily Volume Distribution",
            "📦 Performance by Card Type",
            "📅 Performance by Day of Week",
            "🥧 Card Type Breakdown"
        ),
        row_heights=[0.30, 0.35, 0.35],
        vertical_spacing=0.12,
        horizontal_spacing=0.10
    )

    # 1. Relearn Rate
    fig.add_trace(create_relearn_rate_chart(monthly_df), row=1, col=1)

    # 2. Distribution
    fig.add_trace(create_distribution_histogram(df), row=1, col=2)

    # 3. Box plots by type
    for trace in create_box_plots_by_type(df):
        fig.add_trace(trace, row=2, col=1)

    # 4. Box plots by weekday
    for trace in create_box_plots_by_weekday(df):
        fig.add_trace(trace, row=2, col=2)

    # 5. Pie chart
    fig.add_trace(create_pie_chart(stats), row=3, col=1)

    # Update layout
    fig.update_layout(
        height=1200,
        showlegend=True,
        margin=dict(l=80, r=80, t=100, b=80),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['paper'],
        font=dict(family=FONT_FAMILY, size=12, color=COLORS['text'])
    )

    # Add grids
    fig.update_xaxes(showgrid=True, gridcolor=COLORS['grid'])
    fig.update_yaxes(showgrid=True, gridcolor=COLORS['grid'])

    return fig


def create_progress_tab(df, stats):
    """Create Progress tab with cumulative and streaks"""

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.50, 0.50],
        specs=[
            [{"type": "scatter"}],
            [{"type": "bar"}],
        ],
        subplot_titles=(
            "📈 Cumulative Progress",
            "🔥 Activity Patterns"
        ),
        vertical_spacing=0.12
    )

    # 1. Cumulative
    for trace in create_cumulative_chart(df):
        fig.add_trace(trace, row=1, col=1)

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
                row=1, col=1
            )

    # 2. Streaks
    for trace in create_streak_visualization(df):
        fig.add_trace(trace, row=2, col=1)

    # Update layout
    fig.update_layout(
        height=1000,
        showlegend=True,
        margin=dict(l=80, r=80, t=100, b=80),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['paper'],
        font=dict(family=FONT_FAMILY, size=12, color=COLORS['text'])
    )

    # Add grids
    fig.update_xaxes(showgrid=True, gridcolor=COLORS['grid'])
    fig.update_yaxes(showgrid=True, gridcolor=COLORS['grid'])

    return fig


def create_html_with_tabs(overview_fig, analysis_fig, progress_fig, stats):
    """Create HTML with Bootstrap tabs"""

    # Convert figures to HTML divs
    overview_html = overview_fig.to_html(include_plotlyjs='cdn', config=PLOTLY_CONFIG, div_id="overview-plot")
    analysis_html = analysis_fig.to_html(include_plotlyjs=False, config=PLOTLY_CONFIG, div_id="analysis-plot")
    progress_html = progress_fig.to_html(include_plotlyjs=False, config=PLOTLY_CONFIG, div_id="progress-plot")

    # Extract only the div content (remove html/body tags)
    overview_div = overview_html.split('<body>')[1].split('</body>')[0] if '<body>' in overview_html else overview_html
    analysis_div = analysis_html.split('<body>')[1].split('</body>')[0] if '<body>' in analysis_html else analysis_html
    progress_div = progress_html.split('<body>')[1].split('</body>')[0] if '<body>' in progress_html else progress_html

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anki Study Analytics Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: {FONT_FAMILY};
            background-color: #f8f9fa;
            padding: 20px;
        }}
        .dashboard-header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .dashboard-header h1 {{
            font-size: 2.5rem;
            color: #212121;
            margin-bottom: 10px;
        }}
        .dashboard-header p {{
            color: #757575;
            font-size: 1.1rem;
        }}
        .nav-tabs {{
            border-bottom: 2px solid #dee2e6;
            margin-bottom: 30px;
        }}
        .nav-tabs .nav-link {{
            color: #495057;
            font-weight: 500;
            padding: 12px 24px;
            border: none;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }}
        .nav-tabs .nav-link:hover {{
            border-bottom-color: #2196F3;
            color: #2196F3;
        }}
        .nav-tabs .nav-link.active {{
            color: #2196F3;
            background-color: transparent;
            border-bottom-color: #2196F3;
            font-weight: 600;
        }}
        .tab-content {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stats-summary {{
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #2196F3;
        }}
        .stat-label {{
            color: #757575;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="dashboard-header">
            <h1>📚 Anki Study Analytics Dashboard</h1>
            <p>{stats["date_range"]}</p>
        </div>

        <ul class="nav nav-tabs" id="dashboardTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="overview-tab" data-bs-toggle="tab"
                        data-bs-target="#overview" type="button" role="tab">
                    📊 Overview
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="analysis-tab" data-bs-toggle="tab"
                        data-bs-target="#analysis" type="button" role="tab">
                    🔍 Analysis
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="progress-tab" data-bs-toggle="tab"
                        data-bs-target="#progress" type="button" role="tab">
                    📈 Progress
                </button>
            </li>
        </ul>

        <div class="tab-content" id="dashboardTabContent">
            <div class="tab-pane fade show active" id="overview" role="tabpanel">
                {overview_div}
            </div>
            <div class="tab-pane fade" id="analysis" role="tabpanel">
                {analysis_div}
            </div>
            <div class="tab-pane fade" id="progress" role="tabpanel">
                {progress_div}
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Resize plots when tab is shown
        document.querySelectorAll('button[data-bs-toggle="tab"]').forEach(button => {{
            button.addEventListener('shown.bs.tab', function (e) {{
                window.dispatchEvent(new Event('resize'));
            }});
        }});
    </script>
</body>
</html>
"""

    return html_template


def main():
    """Main execution function"""
    print("=" * 60)
    print("Anki Study Analytics Dashboard Generator (Tabbed)")
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

    # Create tabs
    print("\n🎨 Building dashboard tabs...")
    print("  Creating Overview tab...")
    overview_fig = create_overview_tab(df, stats, monthly_df)

    print("  Creating Analysis tab...")
    analysis_fig = create_analysis_tab(df, monthly_df, stats)

    print("  Creating Progress tab...")
    progress_fig = create_progress_tab(df, stats)

    # Combine into HTML with tabs
    print("  Assembling tabbed dashboard...")
    html_content = create_html_with_tabs(overview_fig, analysis_fig, progress_fig, stats)

    # Save to HTML
    output_path = os.path.join(SCRIPT_DIR, 'anki_dashboard.html')
    print(f"\n💾 Saving dashboard to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_size = os.path.getsize(output_path) / 1024 / 1024  # MB
    print(f"   File size: {file_size:.2f} MB")

    print("\n✅ Dashboard created successfully!")
    print(f"   Open in browser: file://{output_path}")
    print("\n" + "=" * 60)

    # Optionally open in browser
    import webbrowser
    webbrowser.open(f'file://{output_path}')


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
