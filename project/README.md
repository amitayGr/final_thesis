# Integrated Geometry Learning System

A unified system combining a user-friendly frontend with an intelligent adaptive geometry learning backend.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Logging](#logging)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project integrates two Flask applications:

1. **Frontend Service** (Port 5000): User interface with authentication, user management, and UI rendering
2. **Backend Service** (Port 5001): Adaptive geometry learning API with intelligent question selection

### Key Features

- ✅ **Separate Databases**: User management and learning analytics remain in separate databases
- ✅ **RESTful API Integration**: Frontend calls backend API for all geometry learning functionality
- ✅ **Comprehensive Logging**: Clear service identification with [FRONTEND] and [BACKEND] prefixes
- ✅ **Adaptive Learning**: Entropy-based question selection and dynamic weight adjustment
- ✅ **User Management**: Complete authentication and profile system

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────┐
│   Frontend Service (Port 5000)  │
│   ─────────────────────────────  │
│   • User Authentication          │
│   • UI Rendering                 │
│   • Session Management           │
│   • User Database                │
└────────┬────────────────────────┘
         │ HTTP API Calls
         ↓
┌─────────────────────────────────┐
│   Backend Service (Port 5001)   │
│   ─────────────────────────────  │
│   • Question Selection           │
│   • Answer Processing            │
│   • Weight Management            │
│   • Theorem Recommendations      │
│   • Geometry Learning Database   │
└─────────────────────────────────┘
```

---

## 📁 Project Structure

```
project/
├── backend_service/           # Backend API service
│   ├── app.py                # Flask API server
│   ├── config.py             # Backend configuration
│   ├── geometry_manager.py   # Core learning engine
│   ├── session.py            # Session data model
│   ├── session_db.py         # Session database interface
│   ├── geometry_learning.db  # Geometry learning database
│   ├── sessions.db           # Learning sessions database
│   ├── requirements.txt      # Backend dependencies
│   └── test_api.py           # API testing script
│
├── frontend_service/          # Frontend web service
│   ├── app.py                # Flask web server
│   ├── config.py             # Frontend configuration
│   ├── backend_client.py     # Backend API client
│   ├── auth_config.py        # Authentication config
│   ├── db_config.py          # Database config
│   ├── db_utils.py           # Database utilities
│   ├── email_utils.py        # Email utilities
│   ├── extensions.py         # Flask extensions
│   ├── UserLogger.py         # User logging
│   ├── requirements.txt      # Frontend dependencies
│   ├── pages/                # Page blueprints
│   │   ├── Home_Page/
│   │   ├── Login_Page/
│   │   ├── Registration_Page/
│   │   ├── Question_Page/
│   │   ├── Feedback_Page/
│   │   ├── Contact_Page/
│   │   └── User_Profile_Page/
│   ├── static/               # Static files (CSS, JS, images)
│   ├── templates/            # HTML templates
│   └── flask_session/        # Session storage
│
├── logs/                      # Application logs
│   ├── backend_service.log   # Backend logs
│   ├── frontend_service.log  # Frontend logs
│   └── .gitignore
│
├── .env.example              # Environment variables template
└── README.md                 # This file
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone or Navigate to Project

```bash
cd c:\Users\lahavor\am\final_thesis\project
```

### 2. Set Up Backend Service

```powershell
# Navigate to backend directory
cd backend_service

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend Service

```powershell
# Navigate to frontend directory
cd ..\frontend_service

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Copy `.env.example` to `.env` and modify as needed:

```powershell
Copy-Item ..\\.env.example .env
```

Edit `.env` to change:
- Secret keys
- Port numbers
- Database paths
- Log levels

---

## ▶️ Running the Application

You need to run **both services** simultaneously in separate terminals.

### Terminal 1: Start Backend Service

```powershell
cd c:\Users\lahavor\am\final_thesis\project\backend_service
python app.py
```

You should see:
```
[2025-11-12 10:00:00] [BACKEND] [INFO] - Backend service starting...
[2025-11-12 10:00:00] [BACKEND] [INFO] - Starting backend service on 0.0.0.0:5001
 * Running on http://0.0.0.0:5001
```

### Terminal 2: Start Frontend Service

```powershell
cd c:\Users\lahavor\am\final_thesis\project\frontend_service
python app.py
```

You should see:
```
[2025-11-12 10:00:05] [FRONTEND] [INFO] - Frontend service starting...
[2025-11-12 10:00:05] [FRONTEND] [INFO] - Starting frontend service on 0.0.0.0:5000
 * Running on http://0.0.0.0:5000
```

### Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:5001/api/health

---

## 📚 API Documentation

### Backend Service Endpoints

All endpoints are prefixed with `/api`

#### Health Check
```
GET /api/health
```
Returns backend service status.

#### Session Management
```
GET  /api/start              # Initialize new session
POST /api/session/end        # End session with feedback
GET  /api/session/state      # Get current session state
```

#### Questions
```
GET /api/question/first      # Get first question
GET /api/question/next       # Get next question
GET /api/answers             # Get available answer options
```

#### Answer Processing
```
POST /api/answer
Body: {
  "question_id": int,
  "answer_id": int
}
```

#### Theorems
```
GET /api/theorems?question_id=X&answer_id=Y&base_threshold=0.01
```

### Example API Usage

```python
import requests

# Start session
response = requests.get("http://localhost:5001/api/start")
session_id = response.json()["session_id"]

# Get first question
response = requests.get("http://localhost:5001/api/question/first")
question = response.json()

# Process answer
response = requests.post(
    "http://localhost:5001/api/answer",
    json={
        "question_id": question["question_id"],
        "answer_id": 1
    }
)
```

---

## 📊 Logging

### Log Files

- **Backend**: `logs/backend_service.log`
- **Frontend**: `logs/frontend_service.log`

### Log Format

```
[YYYY-MM-DD HH:MM:SS] [SERVICE] [LEVEL] - Message
```

### Example Logs

**Backend:**
```
[2025-11-12 10:30:15] [BACKEND] [INFO] - Session initialized: session_id=abc-123
[2025-11-12 10:30:20] [BACKEND] [INFO] - Question selected: question_id=5, method=information_gain
[2025-11-12 10:30:25] [BACKEND] [INFO] - Answer processed: question_id=5, answer_id=1
[2025-11-12 10:30:30] [BACKEND] [INFO] - Triangle weights updated: {0: 0.15, 1: 0.25, 2: 0.35, 3: 0.25}
```

**Frontend:**
```
[2025-11-12 10:30:10] [FRONTEND] [INFO] - User logged in: user_id=42, username=john_doe
[2025-11-12 10:30:15] [FRONTEND] [INFO] - Calling backend: POST /api/start
[2025-11-12 10:30:15] [FRONTEND] [INFO] - Backend response: session initialized successfully
[2025-11-12 10:30:20] [FRONTEND] [INFO] - Calling backend: GET /api/question/next
```

### Adjusting Log Levels

Edit `.env` file:
```env
BACKEND_LOG_LEVEL=DEBUG    # DEBUG, INFO, WARNING, ERROR
FRONTEND_LOG_LEVEL=INFO
```

---

## 🧪 Testing

### Test Backend API

```powershell
cd backend_service
python test_api.py
```

This will:
1. ✅ Check health endpoint
2. ✅ Test complete session flow
3. ✅ Test error handling
4. ✅ Verify all endpoints

### Manual Testing

1. **Health Check**:
   ```powershell
   curl http://localhost:5001/api/health
   ```

2. **Start Session**:
   ```powershell
   curl http://localhost:5001/api/start
   ```

3. **Frontend Access**:
   - Open http://localhost:5000
   - Register a new user
   - Login
   - Navigate to Question page
   - Verify questions load from backend

---

## 🔧 Troubleshooting

### Backend Service Won't Start

**Problem**: `Port 5001 already in use`

**Solution**:
```powershell
# Find process using port
netstat -ano | findstr :5001

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Frontend Can't Connect to Backend

**Problem**: `Connection refused` or `Backend service unavailable`

**Checklist**:
1. ✅ Backend service is running
2. ✅ Backend is on correct port (5001)
3. ✅ No firewall blocking localhost
4. ✅ Check `BACKEND_SERVICE_URL` in config

**Solution**:
```python
# In frontend_service/config.py
BACKEND_SERVICE_URL = 'http://localhost:5001'  # Not 127.0.0.1
```

### Database Errors

**Problem**: `no such table` or `database locked`

**Solution**:
```powershell
# Verify databases exist
cd backend_service
dir *.db

# If missing, copy from original backend directory
Copy-Item ..\..\backend\geometry_learning.db .
Copy-Item ..\..\backend\sessions.db .
```

### Session Not Persisting

**Problem**: Session data lost between requests

**Solution**:
```powershell
# Ensure flask_session directory exists
cd frontend_service
mkdir flask_session -Force
```

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**:
```powershell
# Ensure you're in correct directory and venv is activated
cd backend_service  # or frontend_service
pip install -r requirements.txt
```

### Logs Not Being Created

**Problem**: No log files in `logs/` directory

**Solution**:
```powershell
# Ensure logs directory exists
cd ..
mkdir logs -Force

# Check permissions
# Logs will be created automatically on first run
```

---

## 🔐 Security Notes

### Important for Production

1. **Change Secret Keys**: Update both `BACKEND_SECRET_KEY` and `FRONTEND_SECRET_KEY`
2. **Use HTTPS**: Configure SSL/TLS certificates
3. **Database Security**: Move databases outside web root
4. **Environment Variables**: Never commit `.env` to version control
5. **CORS Configuration**: Restrict allowed origins in production

### Development vs Production

**Development** (current setup):
- Debug mode enabled
- Detailed error messages
- CORS allows all origins
- Logs to files and console

**Production** (recommended changes):
- Set `DEBUG=False`
- Use production WSGI server (gunicorn, uwsgi)
- Restrict CORS origins
- Use environment variables for secrets
- Set up log rotation

---

## 📝 Database Information

### Backend Databases

#### geometry_learning.db
Contains:
- Questions table
- Triangles table
- Theorems table
- TheoremTriangleMatrix
- DynamicAnswerMultipliers
- TheoremScores
- QuestionPrerequisites

#### sessions.db
Contains:
- Learning session history
- Student interactions
- Feedback data

### Frontend Database

Contains (managed separately):
- Users table
- Authentication data
- User profiles
- User preferences

**Note**: Databases are **NOT merged** - they remain completely separate.

---

## 🤝 Contributing

### Making Changes

1. **Backend Logic**: Modify files in `backend_service/`
2. **Frontend UI**: Modify files in `frontend_service/pages/`, `templates/`, `static/`
3. **API Integration**: Modify `backend_client.py`

### Testing Changes

1. Make your changes
2. Run backend service
3. Run frontend service
4. Run `test_api.py`
5. Check logs for errors

---

## 📄 License

[Your License Here]

---

## 👥 Authors

- **Original Backend**: [Backend Team]
- **Original Frontend**: [Frontend Team]
- **Integration**: [Your Name]

---

## 📞 Support

For issues or questions:
- Check logs in `logs/` directory
- Review [Troubleshooting](#troubleshooting) section
- Run `test_api.py` to diagnose backend issues

---

**Last Updated**: November 12, 2025
