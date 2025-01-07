import pandas as pd
import numpy as np


class ExerciseRecommender:
    def __init__(self):
        self.exercise_data = pd.read_csv('data/exercise_data.csv')

    def get_difficulty_level(self, bmi, activity_level):
        """Determine the appropriate difficulty level based on BMI and activity level"""
        if activity_level == "Sedentary":
            return "Beginner"
        elif activity_level in ["Lightly Active", "Moderately Active"]:
            return "Intermediate"
        else:
            return "Advanced"

    def recommend_exercises(self, bmi, activity_level, goal, health_conditions=None):
        """Recommend exercises based on user parameters"""
        difficulty = self.get_difficulty_level(bmi, activity_level)

        # Filter exercises based on difficulty
        suitable_exercises = self.exercise_data[
            self.exercise_data['Difficulty'].str.lower() <= difficulty.lower()]

        # Adjust recommendations based on goal
        if goal == "Weight Loss":
            suitable_exercises = suitable_exercises[
                suitable_exercises['Category'].isin(['Cardio', 'HIIT'])]
        elif goal == "Muscle Gain":
            suitable_exercises = suitable_exercises[
                suitable_exercises['Category'].isin(['Strength'])]
        elif goal == "Flexibility":
            suitable_exercises = suitable_exercises[
                suitable_exercises['Category'].isin(['Flexibility', 'Core'])]

        # Filter based on health conditions if specified
        if health_conditions and 'None' not in health_conditions:
            # Add specific exercise filtering logic for health conditions
            if 'Joint Pain' in health_conditions:
                suitable_exercises = suitable_exercises[
                    ~suitable_exercises['Category'].isin(['HIIT', 'High Impact'])]
            if 'Heart Condition' in health_conditions:
                suitable_exercises = suitable_exercises[
                    suitable_exercises['Category'] != 'HIIT']

        # Get available categories
        cardio = suitable_exercises[suitable_exercises['Category'].isin(['Cardio', 'HIIT'])]
        strength = suitable_exercises[suitable_exercises['Category'] == 'Strength']
        other = suitable_exercises[~suitable_exercises['Category'].isin(['Cardio', 'HIIT', 'Strength'])]

        # Sample only if data is available
        result = []

        if not cardio.empty:
            result.append(cardio.sample(min(2, len(cardio))))
        if not strength.empty:
            result.append(strength.sample(min(2, len(strength))))
        if not other.empty:
            result.append(other.sample(min(1, len(other))))

        # If no exercises match the criteria, return some default exercises
        if not result:
            return pd.DataFrame({
                'Exercise': ['Walking', 'Stretching', 'Light Yoga'],
                'Category': ['Cardio', 'Flexibility', 'Flexibility'],
                'Difficulty': ['Beginner', 'Beginner', 'Beginner'],
                'CaloriesPerHour': [280, 150, 200],
                'TargetMuscles': ['Lower Body', 'Full Body', 'Full Body']
            })

        return pd.concat(result) if result else pd.DataFrame()

    def create_workout_plan(self, exercises, duration_minutes=30):
        """Create a workout plan with specified exercises and duration"""
        workout_plan = []

        if exercises.empty:
            return workout_plan

        # Calculate time per exercise
        time_per_exercise = max(5, duration_minutes // len(exercises))

        for _, exercise in exercises.iterrows():
            calories = round((exercise['CaloriesPerHour'] * time_per_exercise) / 60)
            workout_plan.append({
                'exercise': exercise['Exercise'],
                'duration': time_per_exercise,
                'calories': calories,
                'target_muscles': exercise['TargetMuscles'],
                'difficulty': exercise['Difficulty']
            })

        return workout_plan

    def calculate_total_calories(self, workout_plan):
        """Calculate total calories burned in the workout"""
        return sum(workout['calories'] for workout in workout_plan)

    def get_exercise_tips(self, exercise_name):
        """Get tips for specific exercises"""
        exercise_tips = {
            'Walking': [
                "Keep a steady pace",
                "Maintain good posture",
                "Swing arms naturally"
            ],
            'Jogging': [
                "Land softly on your feet",
                "Keep a consistent breathing pattern",
                "Look straight ahead"
            ],
            # Add more exercise tips as needed
        }
        return exercise_tips.get(exercise_name, ["Focus on proper form", "Breathe steadily", "Stay hydrated"])
