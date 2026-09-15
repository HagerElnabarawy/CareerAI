# CareerAI 🤖

CareerAI is an AI-powered career development platform built with Django and a local Generative AI model.

The platform helps users analyze their CV, discover suitable career paths, identify missing skills, generate a personalized learning roadmap, practice job interviews, and communicate with an AI career assistant.

## ✨ Features

### 🔐 Authentication
- User registration
- User login and logout
- Protected dashboard
- User-specific career data

### 📄 CV Analysis
- Upload CV as a PDF
- Extract text from the uploaded CV
- Analyze CV using Generative AI
- Recommend a suitable career path
- Identify strengths
- Identify missing skills
- Provide career analysis

### 🗺️ AI Learning Roadmap
- Generate a personalized learning roadmap
- AI-generated learning steps
- Track roadmap progress
- Mark learning steps as completed

### 🎤 AI Mock Interview
- Generate interview questions using AI
- Submit interview answers
- Receive an AI-generated score
- Get feedback
- Identify strengths and areas for improvement
# CareerAI 🤖

CareerAI is an AI-powered career development platform built with Django and a local Generative AI model.

The platform helps users analyze their CV, discover suitable career paths, identify missing skills, generate a personalized learning roadmap, practice job interviews, and communicate with an AI career assistant.

## ✨ Features

### 🔐 Authentication
- User registration
- User login and logout
- Protected dashboard
- User-specific career data

### 📄 CV Analysis
- Upload CV as a PDF
- Extract text from the uploaded CV
- Analyze CV using Generative AI
- Recommend a suitable career path
- Identify strengths
- Identify missing skills
- Provide career analysis

### 🗺️ AI Learning Roadmap
- Generate a personalized learning roadmap
- AI-generated learning steps
- Track roadmap progress
- Mark learning steps as completed

### 🎤 AI Mock Interview
- Generate interview questions using AI
- Submit interview answers
- Receive an AI-generated score
- Get feedback
- Identify strengths and areas for improvement

### 💬 AI Career Assistant
- Interactive AI chat
- Career-related questions and guidance
- Conversation history stored per user
- Supports Arabic and English conversations

## 🤖 Generative AI

CareerAI uses a locally running Generative AI model through Ollama.

### AI Stack

- Ollama
- Qwen3:8b
- Local HTTP API
- Python `urllib`
- JSON-based AI responses

Using a local AI model allows the application to run AI features without depending on external AI API quotas.

## 🛠️ Technologies

### Backend
- Python
- Django
- SQLite

### AI
- Ollama
- Qwen3:8b
- Generative AI

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### PDF Processing
- pypdf

### Development Tools
- VS Code
- Git
- GitHub
- Ubuntu Linux

## 📁 Project Structure

```text
CareerAI/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── ai/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── career/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── accounts/
│   ├── ai/
│   └── career/
│
├── manage.py
├── requirements.txt
└── README.md
