# modules/diet_recommendation.py

import pandas as pd
import numpy as np

class DietRecommender:
    def __init__(self):
        self.food_data = pd.read_csv('data/food_database.csv')

    def calculate_calories_needed(self, weight, height, age, gender, activity_level):
        # Harris-Benedict equation for BMR
        if gender.lower() == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Activity multipliers
        activity_multipliers = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extra Active": 1.9
        }

        daily_calories = bmr * activity_multipliers[activity_level]
        return round(daily_calories)

    def get_meal_plan(self, total_calories, health_preference=None, meal_type='all'):
        breakfast_cals = total_calories * 0.3
        lunch_cals = total_calories * 0.4
        dinner_cals = total_calories * 0.3

        meal_plan = {
            'breakfast': self.get_meal_options('breakfast', breakfast_cals, health_preference),
            'lunch': self.get_meal_options('lunch', lunch_cals, health_preference),
            'dinner': self.get_meal_options('dinner', dinner_cals, health_preference)
        }
        return meal_plan

    def get_meal_options(self, meal_type, target_calories, health_preference=None):
        # Filter foods by meal type
        meal_foods = self.food_data[self.food_data['Category'].str.contains(meal_type, case=False)]

        # Apply health preference filter if specified
        if health_preference and health_preference != "None":
            if health_preference == "Vegetarian":
                meal_foods = meal_foods[~meal_foods['Food'].str.contains('Chicken|Fish|Beef|Pork', case=False, na=False)]
            elif health_preference == "Vegan":
                meal_foods = meal_foods[~meal_foods['Food'].str.contains('Chicken|Fish|Beef|Pork|Egg|Milk|Yogurt|Cheese', case=False, na=False)]
            elif health_preference == "Low-Carb":
                meal_foods = meal_foods[meal_foods['Carbohydrates'] < 15]
            elif health_preference == "Keto":
                meal_foods = meal_foods[(meal_foods['Carbohydrates'] < 10) & (meal_foods['Fat'] > 15)]

        # Get foods that fit within the calorie target
        suitable_foods = meal_foods[meal_foods['Calories'] <= target_calories]

        # If no suitable foods found, return default options
        if suitable_foods.empty:
            return [{
                'Food': f'Default {meal_type} option',
                'Calories': target_calories,
                'Protein': 0,
                'Carbohydrates': 0,
                'Fat': 0
            }]

        # Sort by calories and return top 3 options
        return suitable_foods.nlargest(3, 'Calories').to_dict('records')

    def get_nutritional_info(self, food_name):
        """Get detailed nutritional information for a specific food"""
        food_info = self.food_data[self.food_data['Food'] == food_name]
        if not food_info.empty:
            return food_info.iloc[0].to_dict()
        return None
