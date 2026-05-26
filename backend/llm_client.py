import os
from openai import OpenAI
from models import UserBiomarkers

import json

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            timeout=60.0,
        )
        # Using a model that is likely to be available and free/cheap on OpenRouter
        self.model = "meta-llama/llama-3-8b-instruct" 

    def generate_recommendation(self, risk_level: str, risk_summary: str, context: str, user_data: UserBiomarkers, past_feedback: str = "") -> dict:
        try:
            prompt = f"""
            You are an expert health assistant.
            
            User Profile:
            - Age: {user_data.age}
            - Gender: {user_data.gender}
            - Weight: {user_data.weight}
            - BMI: {user_data.bmi}
            - Activity Level: {user_data.activity_level}
            - Cholesterol (Total): {user_data.cholesterol_total}
            - LDL: {user_data.cholesterol_ldl}
            - HDL: {user_data.cholesterol_hdl}
            - Triglycerides: {user_data.triglycerides}
            
            Health Assessment:
            - Risk Level: {risk_level}
            - Summary: {risk_summary}
            
            User's Past AI Feedback (use this to adjust and improve new recommendations):
            {past_feedback if past_feedback else "No previous feedback available."}
            
            Relevant Medical Guidelines (Context):
            {context}
            
            Task:
            Provide highly personalized health recommendations based on the user's profile, risk assessment, guidelines context, and their past feedback.
            
            CRITICAL INSTRUCTIONS for Formatting and Feedback Adaptation:
            - Make the diet and fitness plans EXTREMELY clear, structured, and easy to follow.
            - Use bullet points, daily schedules (e.g., Day 1, Day 2), or specific lists of exercises/foods. Avoid generalizations and long walls of text.
            - Be concrete: mention specific exercises (e.g., "3 sets of 10 pushups") and specific foods or meal ideas.
            - STRONGLY ADAPT TO PAST FEEDBACK: 
              * If the user mentioned specific dietary preferences, cultural diets (e.g., "Indian diet", "non-veg", "vegan", "keto"), or allergies in their feedback, your new diet plan MUST entirely adopt that diet type.
              * If they mentioned fitness preferences, injuries, or intensity levels, you must adjust the workout plan to adhere strictly to those comments.
            
            IMPORTANT: Return the response in raw JSON format with exactly these keys:
            - "fitness": A markdown string with the clear fitness plan.
            - "diet": A markdown string with the clear diet plan.
            - "lifestyle": A markdown string with activity and lifestyle changes (sleep, stress, habits).
            
            Do not include any markdown formatting around the JSON (like ```json). Just return the raw JSON object.
            """
            
            
            import time
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are a helpful health assistant that outputs JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"}
                    )
                    
                    content = response.choices[0].message.content
                    return json.loads(content)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"OpenRouter API Error (Attempt {attempt+1}/{max_retries}): {e}. Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                    else:
                        print(f"OpenRouter API Error (Final Attempt): {e}. Switching to Fallback Mode.")
                        return self.get_fallback_recommendation(risk_level, user_data, past_feedback)
            
        except Exception as e:
            print(f"Error during recommendation generation: {e}. Switching to Fallback Mode.")
            return self.get_fallback_recommendation(risk_level, user_data, past_feedback)

    def get_fallback_recommendation(self, risk_level: str, user_data: UserBiomarkers, past_feedback: str = "") -> dict:
        """Returns pre-written advice when API is unavailable."""
        
        lifestyle_advice = """
        ### 🧘 Lifestyle Changes
        - **Hydration:** Drink at least 8 glasses of water daily.
        - **Sleep:** Aim for 7-9 hours of quality sleep.
        - **Stress:** Practice mindfulness or meditation.
        - **Habits:** Avoid smoking and limit alcohol consumption.
        """

        if risk_level == "High":
            return {
                "fitness": """
                ### 🏋️ Fitness Plan (High Risk)
                - **Start Slow:** Begin with 15-20 mins of low-impact walking daily.
                - **Monitor:** Check your heart rate and blood pressure before and after exercise.
                - **Avoid:** High-intensity interval training (HIIT) until approved by a doctor.
                """,
                "diet": """
                ### 🥗 Diet Plan (High Risk)
                - **Strictly Limit:** Sugar, processed foods, and high-sodium meals.
                - **Focus On:** Leafy greens, lean proteins (chicken, fish), and whole grains.
                - **Portion Control:** Use smaller plates to manage calorie intake.
                """,
                "lifestyle": lifestyle_advice
            }
        
        elif risk_level == "Moderate":
             return {
                "fitness": """
                ### 🏋️ Fitness Plan (Moderate Risk)
                - **Cardio:** 30 minutes of brisk walking or cycling, 5 days a week.
                - **Strength:** Light resistance training 2 days a week.
                - **Activity:** Try to reach 8,000 - 10,000 steps daily.
                """,
                "diet": """
                ### 🥗 Diet Plan (Moderate Risk)
                - **Reduce:** Saturated fats and added sugars.
                - **Increase:** Fiber intake through fruits and vegetables.
                - **Hydration:** Replace sugary drinks with water or herbal tea.
                """,
                "lifestyle": lifestyle_advice
            }
        
        else: # Low Risk
             return {
                "fitness": """
                ### 🏋️ Fitness Plan (Maintenance)
                - **Challenge:** Incorporate HIIT or more advanced strength training.
                - **Frequency:** Aim for 150+ minutes of moderate to vigorous activity per week.
                - **Variety:** Mix cardio, strength, and flexibility exercises.
                """,
                "diet": """
                ### 🥗 Diet Plan (Maintenance)
                - **Balance:** Maintain a balanced diet of macros (Protein, Carbs, Fats).
                - **Timing:** Focus on post-workout nutrition for recovery.
                - **Whole Foods:** Continue prioritizing unprocessed, whole foods.
                """,
                "lifestyle": lifestyle_advice
            }
