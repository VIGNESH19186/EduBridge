# EduBridge AI

> **Learn Without Limits. Understand Without Barriers.**

An AI-powered platform for the challenge **AI for Equitable Education Access**.

EduBridge AI connects a student's specific confusion to the right explanation, at the right level, in the right language — while helping teachers identify learning gaps early using measurable learning data.

This is a complete full-stack application with a FastAPI backend, database, REST APIs, grounded RAG pipeline, JWT authentication, adaptive practice, AI services, teacher analytics, and a responsive frontend.

---

## 📋 Table of Contents

* [Problem & Solution](#problem--solution)
* [Features](#features)
* [Core Workflow](#core-workflow)
* [Architecture](#architecture)
* [Project Structure](#project-structure)
* [Technology Stack](#technology-stack)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Running Locally](#running-locally)
* [Demo Accounts](#demo-accounts)
* [API Documentation](#api-documentation)
* [Testing](#testing)
* [Deployment](#deployment)
* [Security](#security)
* [Hackathon Pitch](#hackathon-pitch)
* [Future Scope](#future-scope)
* [License](#license)

---

# 🎯 Problem & Solution

## Problem

Many students lack access to personalized tutoring and doubt resolution.

When a student gets stuck, traditional learning resources often fail to answer:

* What exactly does the student misunderstand?
* What difficulty level is appropriate?
* Which language should the explanation use?
* Which topic is the student weak in?
* What should the student practice next?

Teachers also struggle to identify students who need help because of limited time and large class sizes.

## Solution

**EduBridge AI** combines AI, RAG, adaptive learning, multilingual support, and teacher analytics into one platform.

### EduBridge AI provides:

* 🤖 Grounded AI doubt solving
* 📚 Retrieval-Augmented Generation (RAG)
* 🎯 Adaptive practice
* 🌐 Multilingual learning
* 📊 Student progress tracking
* 👨‍🏫 Teacher analytics
* 💡 Evidence-based teacher insights
* 🔐 Secure authentication
* 🧠 Personalized recommendations

The AI system is designed to avoid unsupported claims by grounding educational responses in the available knowledge base.

---

# ✨ Features

## 👨‍🎓 Student Features

Students can:

* Register and log in
* Select subjects
* Select preferred language
* Ask academic doubts
* Receive step-by-step explanations
* Select explanation difficulty/level
* View source citations
* Generate practice questions
* Take adaptive quizzes
* Track learning progress
* Identify weak topics
* Receive personalized recommendations
* View learning history

---

## 👨‍🏫 Teacher Features

Teachers can:

* Create and manage classes
* View student performance
* Monitor learning progress
* Analyze class-level performance
* Identify weak topics
* Receive AI-generated insights
* Identify students requiring attention
* Get evidence-based intervention recommendations

Teacher insights are based on measurable learning information rather than unsupported psychological assumptions.

---

## 👨‍💼 Admin Features

Administrators can manage:

* Users
* Students
* Teachers
* Subjects
* Topics
* Educational documents
* Knowledge-base content

---

# 🔄 Core Workflow

```text
Student
   ↓
Login / Registration
   ↓
Select Subject + Language
   ↓
Ask Doubt
   ↓
AI Question Analysis
   ↓
Identify Subject / Topic / Difficulty
   ↓
RAG Knowledge Search
   ↓
Retrieve Relevant Educational Content
   ↓
Generate Grounded Explanation
   ↓
Attach Citations
   ↓
Translate Response
   ↓
Quick Check
   ↓
Adaptive Practice
   ↓
Update Learning Profile
   ↓
Student Analytics
   ↓
Teacher Analytics
   ↓
Teacher Insight Agent
   ↓
Recommended Intervention
   ↓
Student Improvement
   ↓
Continuous Learning Loop
```

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │   HTML/CSS/JS       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     REST API        │
                    │      FastAPI        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │  Database   │  │ AI Services │  │ RAG Pipeline│
       │ PostgreSQL  │  │             │  │             │
       │ / SQLite    │  │ AI Provider │  │ Retrieval   │
       └─────────────┘  └─────────────┘  └─────────────┘
```

### Main components

**Frontend**

* HTML
* CSS
* Vanilla JavaScript
* Chart.js

**Backend**

* FastAPI
* SQLAlchemy
* Pydantic
* JWT authentication

**AI**

* Provider abstraction
* AI question analysis
* Doubt solving
* Practice generation
* Recommendations
* Teacher insights
* Translation

**RAG**

```text
Educational Documents
        ↓
Document Ingestion
        ↓
Chunking
        ↓
Text Processing
        ↓
Retrieval
        ↓
Similarity Matching
        ↓
Relevant Context
        ↓
Grounded AI Response
        ↓
Citation
```

---

# 📁 Project Structure

```text
EduBridge-main/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
│
├── ai/
│   ├── __init__.py
│   │
│   ├── evaluation/
│   │   ├── evaluate.py
│   │   └── test_questions.json
│   │
│   ├── prompts/
│   │   ├── doubt_solver.txt
│   │   ├── explanation.txt
│   │   ├── question_generator.txt
│   │   ├── recommendation.txt
│   │   └── teacher_insight.txt
│   │
│   └── rag/
│       ├── __init__.py
│       ├── chunker.py
│       ├── citation.py
│       ├── ingest.py
│       └── retriever.py
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── analytics.py
│   │   ├── auth.py
│   │   ├── doubts.py
│   │   ├── knowledge.py
│   │   ├── practice.py
│   │   ├── recommendations.py
│   │   ├── students.py
│   │   └── teachers.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── seed.py
│   │
│   ├── models/
│   │   ├── attempt.py
│   │   ├── class_model.py
│   │   ├── document.py
│   │   ├── doubt.py
│   │   ├── question.py
│   │   ├── quiz.py
│   │   ├── recommendation.py
│   │   ├── student.py
│   │   ├── subject.py
│   │   ├── teacher.py
│   │   ├── topic.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── analytics.py
│   │   ├── auth.py
│   │   ├── doubt.py
│   │   ├── practice.py
│   │   ├── quiz.py
│   │   ├── student.py
│   │   └── teacher.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── doubt_solver.py
│   │   ├── embedding_service.py
│   │   ├── practice_generator.py
│   │   ├── rag_service.py
│   │   ├── recommendation_engine.py
│   │   ├── teacher_insights.py
│   │   └── translation_service.py
│   │
│   └── utils/
│       ├── logging.py
│       └── security.py
│
├── docs/
│   ├── api.md
│   ├── architecture.md
│   └── deployment.md
│
├── frontend/
│   ├── index.html
│   ├── assets/
│   ├── css/
│   └── js/
│
├── scripts/
│   ├── setup.py
│   └── seed_database.py
│
└── tests/
    ├── ...
    └── conftest.py
```

---

# 🛠️ Technology Stack

| Layer               | Technology                   |
| ------------------- | ---------------------------- |
| Frontend            | HTML, CSS, JavaScript        |
| Charts              | Chart.js                     |
| Backend             | Python, FastAPI              |
| ORM                 | SQLAlchemy                   |
| Validation          | Pydantic                     |
| Authentication      | JWT                          |
| Password Hashing    | bcrypt / Passlib             |
| Database            | SQLite / PostgreSQL          |
| AI                  | Provider-agnostic AI service |
| Default AI Provider | Anthropic Claude             |
| RAG                 | TF-IDF + Cosine Similarity   |
| ML Library          | scikit-learn                 |
| Containerization    | Docker                       |
| API Documentation   | Swagger / OpenAPI            |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd EduBridge-main
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

You can also run:

```bash
python scripts/setup.py
```

---

# 🔐 Environment Variables

Example:

```env
DATABASE_URL=sqlite:///./edubridge.db

JWT_SECRET_KEY=change-this-super-secret-key-in-production

AI_PROVIDER=anthropic

AI_API_KEY=

AI_MODEL=claude-sonnet-4-6
```

### Demo Mode

An AI API key is not required for local testing.

If no AI API key is configured, the application can run in **Demo Mode** with clearly identified sample AI responses.

For production, configure a secure AI provider/API key.

---

# ▶️ Running Locally

## 1. Seed the database

```bash
python scripts/seed_database.py
```

## 2. Start the FastAPI server

```bash
uvicorn backend.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

The frontend is served by the FastAPI backend.

---

# 📚 API Documentation

After starting the server, open:

```text
http://localhost:8000/docs
```

FastAPI automatically provides an interactive Swagger API interface.

Alternative OpenAPI documentation:

```text
http://localhost:8000/redoc
```

---

# 👤 Demo Accounts

| Role    | Email                 | Password      |
| ------- | --------------------- | ------------- |
| Student | `student@example.com` | `password123` |
| Teacher | `teacher@example.com` | `password123` |

The database seed also creates additional demo students with varied learning-performance data for teacher analytics.

**Do not use these credentials in production.**

---

# 🧪 Testing

Run the complete test suite:

```bash
pytest
```

The project includes tests covering areas such as:

* Authentication
* Role-based access control
* Doubt solving
* RAG retrieval
* Grounding
* Adaptive practice
* Difficulty adjustment
* Teacher analytics
* Teacher insight evidence requirements

## AI Evaluation

Run:

```bash
python ai/evaluation/evaluate.py
```

This evaluates the AI question-classification functionality using the provided test questions.

---

# 🐳 Docker

Build and run the application:

```bash
docker build -t edubridge-ai .
docker run -p 8000:8000 edubridge-ai
```

If Docker Compose configuration is available:

```bash
docker compose up --build
```

---

# 🚀 Deployment

EduBridge AI can be deployed using:

* Vercel — frontend
* Render — backend
* Railway — backend/database
* Google Cloud Run — containerized backend
* PostgreSQL — production database

## Recommended architecture

```text
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │     Vercel      │
              │    Frontend     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     Render      │
              │ FastAPI Backend │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
       ┌─────────────┐   ┌─────────────┐
       │ PostgreSQL  │   │ AI Provider │
       └─────────────┘   └─────────────┘
```

Before deploying:

* Set production environment variables
* Use PostgreSQL
* Generate a strong JWT secret
* Configure CORS
* Configure the AI provider
* Disable demo credentials
* Enable HTTPS
* Do not commit `.env`
* Review API access permissions

---

# 🔒 Security

EduBridge AI uses:

* JWT-based authentication
* Password hashing
* Role-based access control
* Environment-based secrets
* API validation through Pydantic
* Database-backed user management

### Important

Never commit:

```text
.env
```

or production API keys to GitHub.

Use:

```text
.env.example
```

for sharing configuration templates.

---

# 🤖 AI & RAG Pipeline

The platform uses a grounded RAG architecture.

```text
User Question
     ↓
Question Analysis
     ↓
Subject / Topic Detection
     ↓
Knowledge Base Search
     ↓
Document Chunk Retrieval
     ↓
Similarity Ranking
     ↓
Relevant Context
     ↓
AI Prompt
     ↓
Generated Explanation
     ↓
Citation Verification
     ↓
Final Answer
```

The local RAG implementation uses:

```text
TF-IDF
+
Cosine Similarity
```

The retriever architecture can later be extended to:

* FAISS
* ChromaDB
* Vector databases
* Real embedding models

---

# 🌐 Multilingual Learning

EduBridge AI is designed to reduce language barriers by allowing learners to select their preferred language.

The translation service can be integrated with external AI/translation providers while maintaining the same backend service abstraction.

---

# 🎯 Adaptive Learning

The practice system uses student performance to adjust future questions.

Example:

```text
High Accuracy
     ↓
Increase Difficulty
     ↓
More Challenging Questions

Low Accuracy
     ↓
Reduce Difficulty
     ↓
Provide More Fundamental Practice
```

The system can use:

* Accuracy
* Attempts
* Topic performance
* Question difficulty
* Previous learning activity

to improve recommendations.

---

# 👨‍🏫 Teacher Insight System

Teacher analytics transform student learning activity into actionable insights.

```text
Student Attempts
       ↓
Performance Aggregation
       ↓
Topic Analysis
       ↓
Weak Area Detection
       ↓
Teacher Insight Agent
       ↓
Evidence-Based Recommendation
       ↓
Teacher Intervention
```

The system is designed to base recommendations on measurable educational data.

---

# 📊 Example Learning Loop

```text
Student asks:
"Why does photosynthesis need sunlight?"

             ↓

AI identifies:
Subject → Biology
Topic → Photosynthesis
Level → Beginner

             ↓

RAG retrieves:
Relevant educational material

             ↓

AI generates:
Step-by-step explanation

             ↓

Student completes:
Quick knowledge check

             ↓

System measures:
Accuracy + topic performance

             ↓

Adaptive engine generates:
Next practice questions

             ↓

Learning profile updated

             ↓

Teacher dashboard receives:
Updated performance information
```

---

# 🏆 Hackathon Pitch

> **Every student deserves a tutor who explains things their way — grounded in real educational sources, in their language, and at their level. Every teacher deserves to know who needs help before they fall behind, based on evidence rather than guesswork. EduBridge AI makes both possible through grounded AI, adaptive learning, multilingual support, and actionable teacher analytics.**

---

# 🔮 Future Scope

Planned improvements include:

* Replace TF-IDF with advanced embedding models
* ChromaDB / FAISS vector retrieval
* Real-time AI tutoring
* Voice-based doubt solving
* Offline-first mobile application
* Push notifications
* Teacher quiz builder
* Advanced recommendation engine
* Expanded multilingual support
* Advanced admin dashboard
* Learning-path generation
* More sophisticated knowledge graphs
* Student-parent progress reporting

---

# 📄 License

This project is developed for educational and hackathon purposes.

Add the appropriate open-source or institutional license before public production distribution.
