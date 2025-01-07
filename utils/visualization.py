# utils/visualization.py

import plotly.express as px
import plotly.graph_objects as go

def create_progress_gauge(value, max_value, title):
    """Create a gauge chart for progress visualization"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value/2], 'color': "lightgray"},
                {'range': [max_value/2, max_value], 'color': "gray"}
            ]
        }
    ))
    return fig

def create_weekly_calendar(progress_data):
    """Create a calendar heatmap of activity"""
    # Implementation for calendar heatmap
    pass
