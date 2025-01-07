# modules/goal_tracker.py

import pandas as pd
from datetime import datetime, timedelta


class GoalTracker:
    def __init__(self):
        self.goals = pd.DataFrame(columns=[
            'goal_type', 'target_value', 'current_value',
            'start_date', 'target_date', 'status'
        ])

    def add_goal(self, goal_type, target_value, target_date):
        """Add a new goal"""
        new_goal = pd.DataFrame({
            'goal_type': [goal_type],
            'target_value': [target_value],
            'current_value': [0],
            'start_date': [datetime.now().strftime('%Y-%m-%d')],
            'target_date': [target_date],
            'status': ['In Progress']
        })
        self.goals = pd.concat([self.goals, new_goal], ignore_index=True)

    def update_goal_progress(self, goal_type, current_value):
        """Update progress for a specific goal"""
        idx = self.goals[self.goals['goal_type'] == goal_type].index
        if len(idx) > 0:
            self.goals.loc[idx[-1], 'current_value'] = current_value

            # Update status
            target = self.goals.loc[idx[-1], 'target_value']
            if current_value >= target:
                self.goals.loc[idx[-1], 'status'] = 'Achieved'

    def get_goal_progress(self, goal_type):
        """Get progress for a specific goal"""
        goal = self.goals[self.goals['goal_type'] == goal_type].iloc[-1]
        if not goal.empty:
            progress = (goal['current_value'] / goal['target_value']) * 100
            return min(progress, 100)
        return 0

    def get_all_goals(self):
        """Get all active goals"""
        return self.goals[self.goals['status'] == 'In Progress']
