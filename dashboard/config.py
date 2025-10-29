"""
Configuration and constants for Anki Dashboard
"""

import os

# ==============================================================================
# PATHS
# ==============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Root of the project
INPUT_CSV = os.path.join(PROJECT_ROOT, 'data', 'anki_daily_reviews_honest.csv')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'output', 'anki_dashboard.html')

# ==============================================================================
# DASHBOARD SETTINGS
# ==============================================================================

DASHBOARD_TITLE = 'Anki Study Analytics Dashboard'
DASHBOARD_SUBTITLE = 'June 2023 - October 2025'
DASHBOARD_HEIGHT = 6000  # Total height in pixels (increased for better spacing)

# Date range
START_DATE = '2023-06-11'
END_DATE = None  # None = use latest date in data

# ==============================================================================
# COLOR SCHEME
# ==============================================================================

COLORS = {
    # Card types (semantic colors)
    'learning': '#2196F3',    # Blue - new/beginning
    'review': '#4CAF50',      # Green - success/progress
    'total': '#607D8B',       # Gray - neutral/aggregate
    'relearn': '#F44336',     # Red - error/retry

    # UI colors
    'background': '#FFFFFF',  # White
    'paper': '#FAFAFA',       # Very light gray
    'grid': '#E0E0E0',        # Light gray grid
    'text': '#212121',        # Almost black text
    'text_muted': '#757575',  # Gray text

    # Heatmap (GitHub-style greens)
    'heatmap': ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'],

    # Moving averages
    'ma7': '#FF9800',         # Orange
    'ma30': '#9C27B0',        # Purple

    # Streaks
    'streak_active': '#4CAF50',
    'streak_inactive': '#E0E0E0',

    # Gaps
    'gap_short': '#FFC107',   # Amber
    'gap_long': '#F44336',    # Red
}

# ==============================================================================
# TYPOGRAPHY
# ==============================================================================

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_FAMILY_MONO = "'Roboto Mono', 'Courier New', monospace"  # For numbers

FONT_SIZES = {
    'title': 28,
    'subtitle': 20,
    'section': 18,
    'body': 12,
    'small': 10,
}

# ==============================================================================
# LAYOUT
# ==============================================================================

# Row heights for make_subplots (must sum to 1.0)
# Currently using 9 charts (Streak analysis temporarily disabled)
ROW_HEIGHTS = [
    0.10,   # Key metrics (increased)
    0.20,   # Heatmap calendar (increased)
    0.15,   # Monthly time series
    0.10,   # Relearn rate
    0.10,   # Distribution histogram
    0.10,   # Box plots by type
    0.10,   # Box plots by day of week
    0.07,   # Pie chart (slightly increased)
    0.08,   # Cumulative progress
]

VERTICAL_SPACING = 0.05  # 5% spacing between charts (increased for clarity)
HORIZONTAL_SPACING = 0.05

MARGINS = {
    'l': 80,   # Left
    'r': 80,   # Right
    't': 120,  # Top (for title)
    'b': 60,   # Bottom
    'pad': 15  # Padding (increased)
}

# ==============================================================================
# CHART SETTINGS
# ==============================================================================

# Heatmap
HEATMAP_BINS = 5  # Number of color bins
HEATMAP_COLORBAR_TITLE = "Cards<br>Studied"

# Time series
MOVING_AVERAGES = [7, 30]  # Days for moving averages
TIME_SERIES_RANGE_BUTTONS = [
    dict(count=7, label="1w", step="day", stepmode="backward"),
    dict(count=1, label="1m", step="month", stepmode="backward"),
    dict(count=3, label="3m", step="month", stepmode="backward"),
    dict(count=6, label="6m", step="month", stepmode="backward"),
    dict(count=1, label="1y", step="year", stepmode="backward"),
    dict(step="all", label="All")
]

# Distribution
HISTOGRAM_BINS = 30
HISTOGRAM_EXCLUDE_ZEROS = True  # Only show active days

# Box plots
BOX_SHOW_MEAN = True
BOX_SHOW_OUTLIERS = True

# Pie chart
PIE_HOLE = 0.4  # Donut chart (0 = full pie, 0-1 = donut)

# Cumulative
CUMULATIVE_MILESTONES = [10000, 20000, 30000, 40000]  # Show markers at these values

# Streaks
MIN_STREAK_LENGTH = 3  # Minimum days to count as a streak
STREAK_GAP_THRESHOLD = 3  # Days of inactivity to break streak

# ==============================================================================
# INTERACTIVITY
# ==============================================================================

PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'responsive': True,
    'modeBarButtonsToRemove': [
        'pan2d',
        'lasso2d',
        'select2d',
        'autoScale2d'
    ],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'anki_dashboard',
        'height': 1080,
        'width': 1920,
        'scale': 2
    }
}

# Whether to include Plotly.js in HTML
# 'cdn' = small file, requires internet (~50KB)
# True = large file, works offline (~3.5MB)
INCLUDE_PLOTLYJS = 'cdn'

# ==============================================================================
# DATA PROCESSING
# ==============================================================================

# Thresholds
MIN_CARDS_FOR_ACTIVE_DAY = 1  # Minimum cards to count as "active"
OUTLIER_THRESHOLD = 3  # Standard deviations for outlier detection

# ==============================================================================
# EXPORT
# ==============================================================================

# If you want to save individual charts as PNG (requires kaleido)
EXPORT_INDIVIDUAL_CHARTS = False
EXPORT_DIR = os.path.join(SCRIPT_DIR, 'exports')
