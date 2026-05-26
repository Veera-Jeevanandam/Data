import os
from dotenv import load_dotenv
from llm_client import OpenRouterClient
from rag_engine import RAGEngine
from models import UserBiomarkers

load_dotenv()

def test_api():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found.")
        return

    print(f"Testing with API Key: {api_key[:5]}...")
    
    # Test RAG
    print("\nTesting RAG Engine...")
    try:
        rag = RAGEngine(api_key="dummy", knowledge_base_path="data/knowledge_base.txt")
        # Add some dummy data if file doesn't exist or is empty
        if not rag.documents:
            print("Knowledge base empty or missing. Creating dummy data...")
            os.makedirs("data", exist_ok=True)
            with open("data/knowledge_base.txt", "w") as f:
                f.write("High blood pressure is a risk factor for heart disease.\n")
                f.write("Diabetes can be managed with diet and exercise.\n")
            rag = RAGEngine(api_key="dummy", knowledge_base_path="data/knowledge_base.txt")
            
        context = rag.retrieve("blood pressure")
        print(f"RAG Context Retrieved: {context}")
    except Exception as e:
        print(f"RAG Error: {e}")

    # Test LLM
    print("\nTesting LLM Client...")
    try:
        client = OpenRouterClient(api_key=api_key)
        user_data = UserBiomarkers(
            age=30,
            gender="Male",
            height=180,
            weight=80,
            activity_level="Moderate",
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=70,
            cholesterol_total=180,
            cholesterol_hdl=50,
            cholesterol_ldl=100,
            triglycerides=150,
            glucose_fasting=90,
            hba1c=5.0,
            bmi=24.7,
            sleep_hours=7
        )
        recommendation = client.generate_recommendation(
            risk_level="Low",
            risk_summary="Healthy",
            context=context,
            user_data=user_data
        )
        print("\nLLM Recommendation:")
        print(recommendation[:200].encode('ascii', errors='ignore').decode('ascii') + "...")
    except Exception as e:
        print(f"LLM Error: {e}")

if __name__ == "__main__":
    test_api()
