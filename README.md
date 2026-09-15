# CareerAI 🚀

AI-powered career guidance platform built with Django and Generative AI.

CareerAI helps users understand their career path by analyzing their CV, identifying strengths and missing skills, generating personalized learning roadmaps, and practicing job interviews with AI.

---

## ✨ Features

- 🔐 User Registration & Login
- 👤 User Profile
- 📄 CV Upload & PDF Text Extraction
- 🤖 AI-powered CV Analysis
- 🎯 Career Recommendation
- 💪 Strengths Identification
- 📚 Missing Skills Detection
- 🗺️ Personalized Learning Roadmap
- ✅ Roadmap Progress Tracking
- 🎤 AI Mock Interviews
- 💬 AI Career Chat Assistant

---

## 🛠️ Technologies

- Python
- Django
- PostgreSQL
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript
- Ollama
- Qwen3:8B
- pypdf
- Gunicorn
- WhiteNoise

---

## 🧠 AI Integration

CareerAI uses Generative AI through Ollama with the Qwen3:8B model.

The AI is used for:

- CV analysis
- Career recommendations
- Strengths identification
- Missing skills detection
- Personalized learning roadmap generation
- Mock interview questions
- Interview scoring and feedback
- Career assistance chat

---

## 📸 Screenshots

### 🔐 Login

![Login](screenshots/login.png)

### 📊 Dashboard

![Dashboard](screenshots/dashboard.png)

### 🤖 Career Analysis

![Career Analysis](screenshots/analysis.png)

### 🗺️ Learning Roadmap

![Learning Roadmap](screenshots/roadmap.png)

### 🎤 Mock Interview

![Mock Interview](screenshots/interview.png)

### 💬 AI Career Chat

![AI Chat](screenshots/chat.png)

---

## 📂 Project Structure

```text
CareerAI/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── urls.py
│   └── views.py
│
├── ai/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── career/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── accounts/
│   ├── career/
│   └── ai/
│
├── static/
│
├── screenshots/
│   ├── login.png
│   ├── dashboard.png
│   ├── analysis.png
│   ├── roadmap.png
│   ├── interview.png
│   └── chat.png
│
├── manage.py
├── requirements.txt
└── README.md