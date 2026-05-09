# 🤖 SupportOS: AI-Powered Customer Support Service

SupportOS is a high-end, full-stack AI Customer Support system. It features a stunning **Glassmorphic Dashboard** and an intelligent **FastAPI Backend** that utilizes semantic search for intent mapping and the Llama-3 model for high-fidelity responses.

![SupportOS Showcase](https://via.placeholder.com/1200x600?text=SupportOS+Dashboard+Showcase)

## ✨ Key Features
- **Intelligent Response System**: Uses Groq Llama-3.1 for human-like interactions.
- **Semantic Intent Classification**: Employs local BERT-based embeddings (`all-MiniLM-L6-v2`) to accurately categorize user queries.
- **Human Escalation**: Automatic detection and manual triggers to escalate complex issues to human agents.
- **Modern Dashboard**: Premium React UI with smooth Framer Motion animations and a dark/gold luxury theme.
- **Live Interaction Logs**: Real-time database logging for audit and monitoring.

## 🛠️ Technology Stack
- **Frontend**: React (Vite), Framer Motion, Axios, Lucide Icons.
- **Backend**: Python (FastAPI), SQLAlchemy, SQLite, Uvicorn.
- **AI/ML**: Groq Cloud SDK, Sentence-Transformers, PyTorch.

---

## 💻 Local Development

### 1. Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- A [Groq API Key](https://console.groq.com/)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file in the `backend/` directory:
```text
GROQ_API_KEY=your_actual_key_here
```
Run the server:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🚀 Deployment to Render (Single Service)

This project is optimized to run as a **single unified service** on Render.

1. **GitHub**: Create a new repository and push this entire project.
2. **Render**:
   - Create a **New Web Service**.
   - **Root Directory**: (Leave blank).
   - **Build Command**: 
     ```bash
     cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
3. **Environment Variables**:
   - Add `GROQ_API_KEY` in the Render dashboard.

---

## 📁 Directory Structure
```text
├── backend/
│   ├── main.py          # FastAPI Application Entry
│   ├── chatbot.py       # AI Logic & Intent Classification
│   ├── models.py        # Database Models (SQLAlchemy)
│   ├── requirements.txt # Python Dependencies
│   └── .env             # Environment Variables (Keep Private!)
├── frontend/
│   ├── src/             # React Components & Logic
│   ├── public/          # Static Assets
│   └── package.json     # Node Dependencies
└── README.md            # This Guide
```

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Created for the Programming for AI Assignment 3.*
