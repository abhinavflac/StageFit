# modules/health_analytics.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


class HealthAnalytics:
    def __init__(self):
        self.analytics_data = pd.DataFrame(columns=[
            'date', 'weight', 'bmi', 'calories_consumed',
            'calories_burned', 'workouts', 'water_intake'
        ])

    def add_daily_data(self, weight, bmi, calories_consumed, calories_burned, workouts, water_intake):
        new_data = pd.DataFrame({
            'date': [datetime.now().strftime('%Y-%m-%d')],
            'weight': [weight],
            'bmi': [bmi],
            'calories_consumed': [calories_consumed],
            'calories_burned': [calories_burned],
            'workouts': [workouts],
            'water_intake': [water_intake]
        })
        self.analytics_data = pd.concat([self.analytics_data, new_data], ignore_index=True)

    def get_weight_trend(self):
        fig = px.line(self.analytics_data, x='date', y='weight',
                      title='Weight Trend Over Time')
        fig.update_layout(height=400)
        return fig

    def get_calorie_balance(self):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=self.analytics_data['date'],
            y=self.analytics_data['calories_consumed'],
            name='Calories Consumed'
        ))
        fig.add_trace(go.Bar(
            x=self.analytics_data['date'],
            y=self.analytics_data['calories_burned'],
            name='Calories Burned'
        ))
        fig.update_layout(
            title='Calorie Balance Over Time',
            barmode='group',
            height=400
        )
        return fig

    def get_health_summary(self):
        if len(self.analytics_data) > 0:
            latest = self.analytics_data.iloc[-1]
            week_ago = self.analytics_data.iloc[0] if len(self.analytics_data) == 1 else \
                self.analytics_data.iloc[-7] if len(self.analytics_data) >= 7 else \
                    self.analytics_data.iloc[0]

            weight_change = latest['weight'] - week_ago['weight']
            avg_calories_burned = self.analytics_data['calories_burned'].mean()
            total_workouts = self.analytics_data['workouts'].sum()

            return {
                'weight_change': weight_change,
                'avg_calories_burned': avg_calories_burned,
                'total_workouts': total_workouts
            }
        return None
