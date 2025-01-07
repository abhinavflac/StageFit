import pandas as pd
import plotly.express as px
from datetime import datetime


class ProgressTracker:
    def __init__(self):
        self.progress_data = pd.DataFrame(columns=[
            'date', 'weight', 'bmi', 'workouts_completed',
            'calories_burned', 'measurements'
        ])

    def add_entry(self, weight, height, workouts_completed, calories_burned):
        """Add a new progress entry"""
        bmi = weight / ((height / 100) ** 2)

        new_entry = pd.DataFrame({
            'date': [datetime.now().strftime('%Y-%m-%d')],
            'weight': [weight],
            'bmi': [bmi],
            'workouts_completed': [workouts_completed],
            'calories_burned': [calories_burned]
        })

        self.progress_data = pd.concat([self.progress_data, new_entry], ignore_index=True)

    def get_workout_summary(self):
        """Get summary of workouts and calories"""
        if len(self.progress_data) > 0:
            total_workouts = self.progress_data['workouts_completed'].sum()
            total_calories = self.progress_data['calories_burned'].sum()
            return total_workouts, total_calories
        return 0, 0

    def get_weight_trend(self):
        """Generate weight trend visualization"""
        if len(self.progress_data) > 0:
            fig = px.line(
                self.progress_data,
                x='date',
                y='weight',
                title='Weight Progress Over Time'
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Weight (kg)",
                height=400
            )
            return fig
        return None

    def get_progress_metrics(self):
        """Calculate progress metrics"""
        if len(self.progress_data) >= 2:
            initial = self.progress_data.iloc[0]
            current = self.progress_data.iloc[-1]

            weight_change = current['weight'] - initial['weight']
            bmi_change = current['bmi'] - initial['bmi']

            return {
                'weight_change': weight_change,
                'bmi_change': bmi_change,
                'days_tracked': len(self.progress_data)
            }
        return None
