import os
os.environ["HF_HUB_OFFLINE"] = "1"
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import UserBiomarkers, RecommendationResponse, UserFeedback
from risk_engine import calculate_risk
from rag_engine import RAGEngine
from llm_client import OpenRouterClient

load_dotenv()

app = FastAPI(title="AI Fitness & Diet Recommender")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Engines (Lazy loading or global)
# Prioritize OPENROUTER_API_KEY, fallback to GEMINI_API_KEY if user hasn't updated env var name yet
API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("GEMINI_API_KEY")
rag_engine = None
llm_client = None

# Always initialize LLM Client for fallback support, even if API key is bad/missing
try:
    llm_client = OpenRouterClient(api_key=API_KEY if API_KEY else "dummy_key")
    
    # Initialize RAG Engine (Local Embeddings now, so API key not strictly needed but good for consistency)
    # We pass the API key just to satisfy the signature if needed, or we can remove it from RAGEngine init if we changed it.
    # I changed RAGEngine to not strictly need it but it takes it.
    rag_engine = RAGEngine(api_key=API_KEY if API_KEY else "dummy", knowledge_base_path="data/knowledge_base.txt")
    print("AI Engines Initialized.")

except Exception as e:
    print(f"Initialization Warning: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Fitness & Diet Recommender API"}

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(user_data: UserBiomarkers):
    # 1. Calculate Risk
    risk_level, risk_summary, analysis, risk_score = calculate_risk(user_data)
    
    fitness_rec = "AI recommendations unavailable (Missing API Key)"
    diet_rec = "AI recommendations unavailable (Missing API Key)"
    lifestyle_rec = "AI recommendations unavailable (Missing API Key)"
    
    # 2. RAG + LLM (if available)
    if llm_client and API_KEY:
        try:
            # Load past user feedback to adapt recommendations
            past_feedback_text = ""
            feedback_file = "data/feedback.json"
            if os.path.exists(feedback_file):
                try:
                    with open(feedback_file, "r") as f:
                        fb_data = json.load(f)
                        if fb_data:
                            recent_fbs = fb_data[-5:]
                            past_feedback_text = "\n".join([
                                f"- Rating: {fb['rating']}/5, Helpful: {fb['is_helpful']}, Comments: {fb.get('comments', 'None')}"
                                for fb in recent_fbs
                            ])
                except Exception:
                    pass

            # Retrieve context based on risk summary (only if RAG is active)
            context = ""
            if rag_engine:
                try:
                    context = rag_engine.retrieve(risk_summary)
                except:
                    pass # Ignore RAG errors in fallback mode
            
            # Generate Recommendations (will use fallback if API fails)
            recommendations = llm_client.generate_recommendation(
                risk_level=risk_level,
                risk_summary=risk_summary,
                context=context,
                user_data=user_data,
                past_feedback=past_feedback_text
            )
            
            fitness_rec = recommendations.get("fitness", "No recommendation available.")
            diet_rec = recommendations.get("diet", "No recommendation available.")
            lifestyle_rec = recommendations.get("lifestyle", "No recommendation available.")
            
        except Exception as e:
            fitness_rec = f"System Error: {str(e)}"
            diet_rec = f"System Error: {str(e)}"
            lifestyle_rec = f"System Error: {str(e)}"
    
    return RecommendationResponse(
        risk_level=risk_level,
        risk_score=risk_score,
        risk_summary=risk_summary,
        fitness_recommendations=fitness_rec,
        diet_recommendations=diet_rec,
        lifestyle_recommendations=lifestyle_rec,
        biomarker_analysis=analysis
    )

@app.post("/feedback")
def submit_feedback(feedback: UserFeedback):
    feedback_file = "data/feedback.json"
    os.makedirs("data", exist_ok=True)
    feedback_data = []

    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            try:
                feedback_data = json.load(f)
            except json.JSONDecodeError:
                pass
    
    if not feedback.timestamp:
        feedback.timestamp = datetime.now().isoformat()
        
    feedback_data.append(feedback.model_dump())
    
    with open(feedback_file, "w") as f:
        json.dump(feedback_data, f, indent=4)
        
    return {"status": "success", "message": "Feedback successfully recorded."}

