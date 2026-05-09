from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, chatbot
from models import SessionLocal, init_db
import os

# Initialize Database
init_db()

app = FastAPI(title="AI Customer Support Chatbot")

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QueryRequest(BaseModel):
    query: str

class EscalateRequest(BaseModel):
    interaction_id: int

@app.post("/ask")
async def ask_question(request: QueryRequest, db: Session = Depends(get_db)):
    # Generate AI response
    response_text, intent = chatbot.generate_response(request.query)
    
    # Log interaction
    new_interaction = models.Interaction(
        user_query=request.query,
        bot_response=response_text,
        intent=intent,
        status="resolved"
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    
    return {
        "id": new_interaction.id,
        "response": response_text,
        "intent": intent
    }

@app.post("/escalate")
async def escalate_query(request: EscalateRequest, db: Session = Depends(get_db)):
    interaction = db.query(models.Interaction).filter(models.Interaction.id == request.interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    interaction.status = "escalated"
    db.commit()
    return {"message": "Query successfully escalated to a human agent."}

@app.get("/logs")
async def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.Interaction).order_by(models.Interaction.timestamp.desc()).all()
    return logs

@app.get("/")
async def root():
    # If the frontend is built, serve the index.html
    if os.path.exists("../frontend/dist/index.html"):
        return FileResponse("../frontend/dist/index.html")
    return {"message": "AI Customer Support API is running"}

# Mount the static files from the React build directory
# This should be at the bottom so it doesn't interfere with API routes
if os.path.exists("../frontend/dist"):
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")
    
    # Catch-all route to handle React Router client-side routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if os.path.exists(f"../frontend/dist/{full_path}"):
            return FileResponse(f"../frontend/dist/{full_path}")
        return FileResponse("../frontend/dist/index.html")
