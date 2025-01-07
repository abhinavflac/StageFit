import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from modules.diet_recommendation import DietRecommender
from modules.exercise_recommendation import ExerciseRecommender
from modules.progress_tracker import ProgressTracker
from modules.health_analytics import HealthAnalytics
from modules.goal_tracker import GoalTracker
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Health Recommendation System",
    page_icon="🏥",
    layout="wide"
)


@st.cache_resource
def load_recommenders():
    return {
        'diet': DietRecommender(),
        'exercise': ExerciseRecommender()
    }


def create_bmi_gauge(bmi_value):
    ranges = [(0, 18.5, "Underweight", "#87CEEB"),
              (18.5, 24.9, "Normal", "#90EE90"),
              (25, 29.9, "Overweight", "#FFD700"),
              (30, 40, "Obese", "#FF6B6B")]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "BMI Meter", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 40], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [ranges[0][0], ranges[0][1]], 'color': ranges[0][3]},
                {'range': [ranges[1][0], ranges[1][1]], 'color': ranges[1][3]},
                {'range': [ranges[2][0], ranges[2][1]], 'color': ranges[2][3]},
                {'range': [ranges[3][0], ranges[3][1]], 'color': ranges[3][3]}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': bmi_value
            }
        }
    ))
    fig.update_layout(height=300)
    return fig


def main():
    st.title("🏥 Personal Health Recommendation System")

    # Initialize recommenders
    recommenders = load_recommenders()

    # Initialize session state objects
    if 'progress_tracker' not in st.session_state:
        st.session_state.progress_tracker = ProgressTracker()
    if 'health_analytics' not in st.session_state:
        st.session_state.health_analytics = HealthAnalytics()
    if 'goal_tracker' not in st.session_state:
        st.session_state.goal_tracker = GoalTracker()

    # Sidebar for user inputs
    with st.sidebar:
        st.header("Personal Information")
        name = st.text_input("Name", "")
        age = st.slider("Age", 1, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        st.subheader("Physical Measurements")
        weight = st.number_input("Weight (kg)", 20.0, 200.0, 70.0)
        height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
        bmi = weight / ((height / 100) ** 2)

        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
        )

    # Main content using tabs
    tabs = st.tabs([
        "BMI Calculator",
        "Diet Planner",
        "Exercise Planner",
        "Progress Tracker",
        "Analytics",
        "Goals"
    ])

    # BMI Calculator Tab
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Your Health Metrics")
            st.write(f"BMI: {bmi:.2f}")
            st.write(f"Activity Level: {activity_level}")

            if bmi < 18.5:
                bmi_category = "Underweight"
                recommendation = "Consider increasing your caloric intake and strength training."
            elif 18.5 <= bmi < 25:
                bmi_category = "Normal weight"
                recommendation = "Maintain your healthy lifestyle with balanced diet and regular exercise."
            elif 25 <= bmi < 30:
                bmi_category = "Overweight"
                recommendation = "Focus on portion control and increasing physical activity."
            else:
                bmi_category = "Obese"
                recommendation = "Consult a healthcare provider for a personalized weight management plan."

            st.write(f"BMI Category: {bmi_category}")
            st.write(f"Recommendation: {recommendation}")

        with col2:
            fig = create_bmi_gauge(bmi)
            st.plotly_chart(fig, use_container_width=True)

    # Diet Planner Tab
    with tabs[1]:
        st.header("🍽️ Diet Recommendations")
        daily_calories = recommenders['diet'].calculate_calories_needed(
            weight=weight,
            height=height,
            age=age,
            gender=gender,
            activity_level=activity_level
        )

        st.write(f"Your estimated daily calorie needs: {daily_calories:.0f} calories")
        diet_preference = st.selectbox(
            "Dietary Preference",
            ["None", "Vegetarian", "Vegan", "Low-Carb", "Keto", "Mediterranean"]
        )

        if st.button("Generate Meal Plan"):
            meal_plan = recommenders['diet'].get_meal_plan(daily_calories)
            for meal, foods in meal_plan.items():
                st.subheader(f"{meal.title()} Options")
                for food in foods:
                    st.write(f"- {food['Food']} ({food['Calories']:.0f} calories)")
                    st.write(
                        f"  Protein: {food.get('Protein', 0)}g | Carbs: {food.get('Carbohydrates', 0)}g | Fat: {food.get('Fat', 0)}g")

    # Exercise Planner Tab
    with tabs[2]:
        st.header("🏋️‍♂️ Exercise Recommendations")
        fitness_goal = st.selectbox(
            "What is your fitness goal?",
            ["Weight Loss", "Muscle Gain", "General Fitness", "Flexibility"]
        )
        health_conditions = st.multiselect(
            "Do you have any health conditions?",
            ["None", "Joint Pain", "Back Pain", "Heart Condition", "Asthma"]
        )
        duration = st.slider("Preferred workout duration (minutes)", 15, 60, 30, 15)

        if st.button("Generate Workout Plan"):
            recommended_exercises = recommenders['exercise'].recommend_exercises(
                bmi=bmi,
                activity_level=activity_level,
                goal=fitness_goal,
                health_conditions=health_conditions
            )
            workout_plan = recommenders['exercise'].create_workout_plan(
                recommended_exercises,
                duration_minutes=duration
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("### Warm-up (5-10 mins)")
                st.write("- Light stretching")
                st.write("- Light walking/jogging")

            with col2:
                st.markdown("### Main Workout")
                for workout in workout_plan:
                    st.write(f"**{workout['exercise']}**")
                    st.write(f"- Duration: {workout['duration']} minutes")
                    st.write(f"- Calories: {workout['calories']} kcal")
                    st.write(f"- Target: {workout['target_muscles']}")

            with col3:
                st.markdown("### Cool-down (5-10 mins)")
                st.write("- Light stretching")
                st.write("- Deep breathing")

    # Progress Tracker Tab
    with tabs[3]:
        st.header("📈 Progress Tracking")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Log Today's Progress")
            workouts_completed = st.number_input("Number of workouts completed today", 0, 10, 0)
            calories_burned = st.number_input("Calories burned today", 0, 2000, 0)

            if st.button("Log Progress"):
                st.session_state.progress_tracker.add_entry(
                    weight=weight,
                    height=height,
                    workouts_completed=workouts_completed,
                    calories_burned=calories_burned
                )
                st.success("Progress logged successfully!")

        with col2:
            st.subheader("Progress Overview")
            total_workouts, total_calories = st.session_state.progress_tracker.get_workout_summary()

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Total Workouts", total_workouts)
            metric_col2.metric("Total Calories Burned", f"{total_calories:,} kcal")

            weight_trend = st.session_state.progress_tracker.get_weight_trend()
            if weight_trend:
                st.plotly_chart(weight_trend, use_container_width=True)

    # Analytics Tab
    with tabs[4]:
        st.header("📊 Health Analytics")
        with st.expander("Log Daily Health Data"):
            col1, col2 = st.columns(2)
            with col1:
                calories_consumed = st.number_input("Calories Consumed", 0, 5000, 2000)
                water_intake = st.number_input("Water Intake (glasses)", 0, 20, 8)
            with col2:
                calories_burned = st.number_input("Calories Burned", 0, 3000, 0)
                workouts_done = st.number_input("Workouts Completed", 0, 5, 0)

            if st.button("Log Daily Data"):
                st.session_state.health_analytics.add_daily_data(
                    weight=weight,
                    bmi=bmi,
                    calories_consumed=calories_consumed,
                    calories_burned=calories_burned,
                    workouts=workouts_done,
                    water_intake=water_intake
                )
                st.success("Data logged successfully!")

    # Goals Tab
    with tabs[5]:
        st.header("🎯 Goals & Achievements")
        with st.expander("Set New Goal"):
            col1, col2 = st.columns(2)
            with col1:
                goal_type = st.selectbox(
                    "Goal Type",
                    ["Weight Loss", "Exercise Frequency", "Daily Steps", "Water Intake", "Calorie Control"]
                )
                target_value = st.number_input(
                    "Target Value",
                    min_value=0.0,
                    help="Enter your target value (e.g., target weight or number of workouts)"
                )
            with col2:
                target_date = st.date_input(
                    "Target Date",
                    min_value=datetime.now().date(),
                    value=datetime.now().date() + timedelta(days=30)
                )

            if st.button("Set Goal"):
                st.session_state.goal_tracker.add_goal(
                    goal_type=goal_type,
                    target_value=target_value,
                    target_date=target_date.strftime('%Y-%m-%d')
                )
                st.success(f"New {goal_type} goal set successfully!")


if __name__ == "__main__":
    main()
