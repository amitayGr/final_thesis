# AI Agent Task: Merge Frontend and Backend Projects

## Project Overview
You need to merge two separate Python Flask projects - a frontend application with user management and a backend application with adaptive geometry learning logic - into a unified, integrated system in a new directory called `project`.

---

## Source Projects

### Frontend Project (`frontend/`)
- **Location**: `C:\Users\lahavor\am\final_thesis\frontend`
- **Main File**: `frontend/app.py`
- **Purpose**: User interface, authentication, and user management
- **Database**: User database with authentication tables (users, sessions, etc.)
- **Key Components**:
  - User registration and login system
  - Session management (Flask-Session with filesystem storage)
  - User profiles
  - Page blueprints (Home, Login, Registration, Question, Feedback, Contact, User Profile)
  - Email utilities
  - Database utilities for user management

### Backend Project (`backend/`)
- **Location**: `C:\Users\lahavor\am\final_thesis\backend`
- **Main File**: `backend/app.py`
- **Purpose**: Adaptive geometry learning system with AI-powered question selection
- **Database**: `geometry_learning.db` and `sessions.db` for learning analytics
- **Key Components**:
  - `GeometryManager` class - core adaptive learning engine
  - Question selection algorithms (entropy-based, information gain)
  - Dynamic weight adjustment system
  - Theorem recommendation engine
  - Session tracking for learning analytics
  - Multiple database tables (Questions, Triangles, Theorems, etc.)

### API Documentation
- **Reference**: `C:\Users\lahavor\am\final_thesis\BACKEND_API_DOCUMENTATION.md`
- **Contains**: Comprehensive documentation of all backend endpoints, classes, methods, database schema, and algorithms

---

## Integration Requirements

### Architecture Design

#### 1. **Separate Databases (Critical Requirement)**
- **Frontend Database**: Keep existing user management database
  - User authentication tables
  - User profile information
  - User session data
- **Backend Database**: Keep existing geometry learning databases
  - `geometry_learning.db` (Questions, Theorems, Triangles, etc.)
  - `sessions.db` (Learning session analytics)
- **DO NOT merge databases** - maintain two separate SQLite databases

#### 2. **Service Separation with Clear Responsibilities**

**Frontend Service** (User-facing Flask app):
- Handle all UI rendering (HTML templates)
- Manage user authentication and authorization
- Maintain user sessions
- Serve static files (CSS, JavaScript, media)
- **Make HTTP requests to Backend Service** for all geometry learning functionality
- Port: 5000 (or configurable)

**Backend Service** (API server):
- Expose RESTful API endpoints
- Handle all geometry learning logic using `GeometryManager`
- Process question selection algorithms
- Manage learning session state
- Update dynamic multipliers and weights
- Provide theorem recommendations
- Port: 5001 (or configurable, different from frontend)

#### 3. **API Integration Points**

The frontend should call backend APIs for:
- Starting a new learning session (`/api/start`)
- Getting the first question (`/api/question/first`)
- Getting the next question (`/api/question/next`)
- Processing student answers (`/api/answer`)
- Getting theorem recommendations (`/api/theorems`)
- Ending a session with feedback (`/api/session/end`)

All existing question/learning logic in the frontend should be **removed** and **replaced** with API calls to the backend service.

---

## Implementation Tasks

### Task 1: Project Structure Setup
Create a new directory structure in `C:\Users\lahavor\am\final_thesis\project`:

```
project/
├── backend_service/
│   ├── app.py                    # Backend Flask API server
│   ├── geometry_manager.py       # Copy from backend/
│   ├── session.py                # Copy from backend/
│   ├── session_db.py             # Copy from backend/
│   ├── geometry_learning.db      # Copy from backend/
│   ├── sessions.db               # Copy from backend/
│   ├── requirements.txt          # Backend dependencies
│   └── config.py                 # Backend configuration
│
├── frontend_service/
│   ├── app.py                    # Frontend Flask web server
│   ├── auth_config.py            # Copy from frontend/
│   ├── db_config.py              # Copy from frontend/
│   ├── db_utils.py               # Copy from frontend/
│   ├── email_utils.py            # Copy from frontend/
│   ├── extensions.py             # Copy from frontend/
│   ├── UserLogger.py             # Copy from frontend/
│   ├── backend_client.py         # NEW: HTTP client for backend API calls
│   ├── requirements.txt          # Frontend dependencies
│   ├── config.py                 # Frontend configuration
│   ├── pages/                    # Copy all from frontend/pages/
│   ├── static/                   # Copy all from frontend/static/
│   ├── templates/                # Copy all from frontend/templates/
│   └── flask_session/            # Session storage directory
│
├── logs/
│   ├── backend_service.log       # Backend service logs
│   └── frontend_service.log      # Frontend service logs
│
├── README.md                     # Project documentation
├── docker-compose.yml            # Optional: For containerization
└── .env.example                  # Environment variables template
```

### Task 2: Backend Service Implementation

#### 2.1 Create Backend API Server (`backend_service/app.py`)
- Import `GeometryManager` from `geometry_manager.py`
- Create Flask app with CORS enabled (to allow frontend calls)
- Implement RESTful API endpoints:

**Endpoints to implement:**

```python
# Session Management
GET  /api/start                    # Initialize new session
POST /api/session/end              # End session with feedback

# Question Management  
GET  /api/question/first           # Get first question
GET  /api/question/next            # Get next question based on current state

# Answer Processing
POST /api/answer                   # Process student answer
     Request body: {
         "question_id": int,
         "answer_id": int
     }

# Theorem Recommendations
GET  /api/theorems                 # Get relevant theorems
     Query params: question_id, answer_id

# Session State
GET  /api/session/state            # Get current session state (weights, asked questions)

# Health Check
GET  /api/health                   # Service health status
```

#### 2.2 Session Management
- Use Flask session to store `GeometryManager` state between requests
- Initialize `GeometryManager` on `/api/start`
- Maintain session state across API calls
- Clear session on `/api/session/end`

#### 2.3 Logging Implementation
- Import Python's `logging` module
- Configure logger with name: `"backend_service"`
- Log to: `../logs/backend_service.log`
- Log format: `[%(asctime)s] [BACKEND] [%(levelname)s] - %(message)s`
- Log all API requests, responses, and errors with clear "BACKEND" prefix

**Example logs:**
```
[2025-11-12 10:30:15] [BACKEND] [INFO] - Session initialized: session_id=abc-123
[2025-11-12 10:30:20] [BACKEND] [INFO] - Question selected: question_id=5, method=information_gain
[2025-11-12 10:30:25] [BACKEND] [INFO] - Answer processed: question_id=5, answer_id=1
[2025-11-12 10:30:30] [BACKEND] [INFO] - Triangle weights updated: {0: 0.15, 1: 0.25, 2: 0.35, 3: 0.25}
```

### Task 3: Frontend Service Implementation

#### 3.1 Create Backend Client (`frontend_service/backend_client.py`)
Create a new module to handle all communication with the backend service:

```python
import requests
import logging

class BackendClient:
    """Client for communicating with the backend geometry learning service"""
    
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.logger = logging.getLogger("frontend_service")
    
    def start_session(self):
        """Initialize a new learning session"""
        # Make GET request to /api/start
        # Log request and response
        # Handle errors
        pass
    
    def get_first_question(self):
        """Get the first question"""
        pass
    
    def get_next_question(self):
        """Get the next question based on current state"""
        pass
    
    def process_answer(self, question_id, answer_id):
        """Process student answer"""
        pass
    
    def get_theorems(self, question_id, answer_id):
        """Get relevant theorem recommendations"""
        pass
    
    def end_session(self, feedback_data):
        """End the session with feedback"""
        pass
    
    def get_session_state(self):
        """Get current session state"""
        pass
```

#### 3.2 Update Frontend App (`frontend_service/app.py`)
- Keep all existing user management functionality
- Keep all existing blueprints and routes
- Add backend client initialization
- Pass backend client to relevant blueprints (Question_Page, Feedback_Page)

#### 3.3 Update Question Page (`frontend_service/pages/Question_Page/Question_Page.py`)
- **Remove**: Any existing question selection logic
- **Remove**: Any direct database queries for questions/theorems
- **Replace with**: Calls to `BackendClient` methods
- When user requests a question, call `backend_client.get_next_question()`
- When user submits an answer, call `backend_client.process_answer()`
- When displaying theorems, call `backend_client.get_theorems()`

#### 3.4 Update Feedback Page (`frontend_service/pages/Feedback_Page/Feedback_Page.py`)
- Use `BackendClient.end_session()` to submit feedback
- Keep user feedback storage in frontend database
- Send learning session feedback to backend service

#### 3.5 Logging Implementation
- Import Python's `logging` module
- Configure logger with name: `"frontend_service"`
- Log to: `../logs/frontend_service.log`
- Log format: `[%(asctime)s] [FRONTEND] [%(levelname)s] - %(message)s`
- Log all user actions, backend API calls, and responses with clear "FRONTEND" prefix

**Example logs:**
```
[2025-11-12 10:30:10] [FRONTEND] [INFO] - User logged in: user_id=42, username=john_doe
[2025-11-12 10:30:15] [FRONTEND] [INFO] - Calling backend: POST /api/start
[2025-11-12 10:30:15] [FRONTEND] [INFO] - Backend response: session initialized successfully
[2025-11-12 10:30:20] [FRONTEND] [INFO] - Calling backend: GET /api/question/next
[2025-11-12 10:30:20] [FRONTEND] [INFO] - Backend response: question_id=5 returned
[2025-11-12 10:30:25] [FRONTEND] [ERROR] - Backend API call failed: Connection timeout to http://localhost:5001
```

### Task 4: Configuration Management

#### 4.1 Backend Configuration (`backend_service/config.py`)
```python
import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('BACKEND_SECRET_KEY', 'backend-default-secret')
    HOST = os.environ.get('BACKEND_HOST', '0.0.0.0')
    PORT = int(os.environ.get('BACKEND_PORT', 5001))
    DEBUG = os.environ.get('BACKEND_DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    GEOMETRY_DB_PATH = os.environ.get('GEOMETRY_DB_PATH', 'geometry_learning.db')
    SESSIONS_DB_PATH = os.environ.get('SESSIONS_DB_PATH', 'sessions.db')
    
    # Logging Configuration
    LOG_FILE = os.environ.get('BACKEND_LOG_FILE', '../logs/backend_service.log')
    LOG_LEVEL = os.environ.get('BACKEND_LOG_LEVEL', 'INFO')
    
    # Algorithm Configuration
    ENTROPY_ALPHA = 0.25
    SCALE_FACTOR = 1.5
    THEOREM_THRESHOLD = 0.01
```

#### 4.2 Frontend Configuration (`frontend_service/config.py`)
```python
import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('FRONTEND_SECRET_KEY', 'frontend-default-secret')
    HOST = os.environ.get('FRONTEND_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FRONTEND_PORT', 5000))
    DEBUG = os.environ.get('FRONTEND_DEBUG', 'False').lower() == 'true'
    JSON_AS_ASCII = False
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=5)
    SESSION_FILE_THRESHOLD = 500
    
    # Backend Service Configuration
    BACKEND_SERVICE_URL = os.environ.get('BACKEND_SERVICE_URL', 'http://localhost:5001')
    BACKEND_TIMEOUT = int(os.environ.get('BACKEND_TIMEOUT', 30))
    
    # Logging Configuration
    LOG_FILE = os.environ.get('FRONTEND_LOG_FILE', '../logs/frontend_service.log')
    LOG_LEVEL = os.environ.get('FRONTEND_LOG_LEVEL', 'INFO')
    
    # Email Configuration (if used)
    # ... existing email config ...
```

#### 4.3 Environment Variables (`.env.example`)
```env
# Backend Service
BACKEND_SECRET_KEY=your-backend-secret-key
BACKEND_HOST=0.0.0.0
BACKEND_PORT=5001
BACKEND_DEBUG=False
BACKEND_LOG_LEVEL=INFO

# Frontend Service
FRONTEND_SECRET_KEY=your-frontend-secret-key
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=5000
FRONTEND_DEBUG=False
FRONTEND_LOG_LEVEL=INFO
BACKEND_SERVICE_URL=http://localhost:5001

# Database Paths
GEOMETRY_DB_PATH=backend_service/geometry_learning.db
SESSIONS_DB_PATH=backend_service/sessions.db
```

### Task 5: Dependencies Management

#### 5.1 Backend Requirements (`backend_service/requirements.txt`)
```txt
Flask==3.0.0
Flask-CORS==4.0.0
```

#### 5.2 Frontend Requirements (`frontend_service/requirements.txt`)
```txt
Flask==3.0.0
Flask-Session==0.5.0
Flask-Bcrypt==1.0.1
requests==2.31.0
# ... other existing frontend dependencies ...
```

### Task 6: Logging Setup

#### 6.1 Create Logs Directory
- Create `project/logs/` directory
- Add `.gitignore` to exclude log files from version control

#### 6.2 Logging Best Practices
- **Every API call** should be logged with request details
- **Every database operation** should be logged
- **Every error** should be logged with full traceback
- **Timing information** for performance monitoring
- **User actions** in frontend (login, logout, question requests)
- **Backend operations** (question selection, weight updates, theorem calculations)

**Key logging points:**

**Backend:**
- Session initialization
- Question selection (with selection method and criteria)
- Answer processing (with weights before/after)
- Theorem recommendation calculations
- Database queries and updates
- Algorithm decisions (entropy calculations, information gain)
- Errors and exceptions

**Frontend:**
- User authentication events
- Page navigation
- Backend API calls (request + response)
- Form submissions
- Session management
- Errors and exceptions

### Task 7: Error Handling and Resilience

#### 7.1 Backend Error Handling
- Validate all input parameters
- Return proper HTTP status codes
- Return JSON error responses with clear messages
- Handle database connection errors
- Log all errors with full context

**Example error response:**
```json
{
    "error": "Question not found",
    "message": "Question with ID 999 does not exist in the database",
    "status": 404
}
```

#### 7.2 Frontend Error Handling
- Handle backend service unavailability gracefully
- Show user-friendly error messages
- Implement retry logic for transient failures
- Fallback UI when backend is down
- Log all errors for debugging

**Example error handling in BackendClient:**
```python
try:
    response = requests.get(f"{self.base_url}/api/question/next", timeout=30)
    response.raise_for_status()
    self.logger.info(f"[FRONTEND] Backend response: {response.json()}")
    return response.json()
except requests.exceptions.Timeout:
    self.logger.error("[FRONTEND] Backend request timeout")
    return {"error": "Backend service timeout"}
except requests.exceptions.ConnectionError:
    self.logger.error("[FRONTEND] Cannot connect to backend service")
    return {"error": "Backend service unavailable"}
except Exception as e:
    self.logger.error(f"[FRONTEND] Unexpected error: {str(e)}")
    return {"error": "Internal error"}
```

### Task 8: Testing and Validation

#### 8.1 Backend Service Testing
Create a simple test script to validate backend API:

```python
# backend_service/test_api.py
import requests

BASE_URL = "http://localhost:5001"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Health check: {response.json()}")

def test_session_flow():
    # Start session
    response = requests.get(f"{BASE_URL}/api/start")
    print(f"Start session: {response.json()}")
    
    # Get first question
    response = requests.get(f"{BASE_URL}/api/question/first")
    print(f"First question: {response.json()}")
    
    # Process answer
    response = requests.post(f"{BASE_URL}/api/answer", 
                           json={"question_id": 1, "answer_id": 1})
    print(f"Process answer: {response.json()}")
    
    # Get next question
    response = requests.get(f"{BASE_URL}/api/question/next")
    print(f"Next question: {response.json()}")

if __name__ == "__main__":
    test_health()
    test_session_flow()
```

#### 8.2 Integration Testing
- Verify frontend can communicate with backend
- Test complete user flow (login → question → answer → feedback)
- Verify logs are being written correctly with proper prefixes
- Confirm databases remain separate and are accessed correctly

### Task 9: Documentation

#### 9.1 Create README.md
Document:
- Project structure
- How to set up both services
- How to run the application
- Environment variable configuration
- Database management
- Logging locations
- API endpoints
- Troubleshooting guide

#### 9.2 Architecture Diagram
Include a simple ASCII diagram showing:
```
User Browser
     ↓
Frontend Service (Port 5000)
     ├── User Management (Frontend DB)
     └── API Calls →
                    ↓
          Backend Service (Port 5001)
               └── Geometry Learning Logic (Backend DBs)
```

---

## Success Criteria

### Functional Requirements ✓
1. **Two separate services** running on different ports
2. **Frontend** handles all user management and UI
3. **Backend** handles all geometry learning logic
4. **Databases remain separate** - no merging
5. **Frontend calls backend API** for all learning functionality
6. **All backend logic** comes from `backend/` directory
7. **Logging** implemented with clear prefixes (FRONTEND/BACKEND)

### Quality Requirements ✓
1. Code is well-organized and follows Python best practices
2. Error handling is comprehensive
3. Logging is detailed and helpful for debugging
4. Configuration is externalized to environment variables
5. Documentation is clear and complete
6. The system is maintainable and extensible

### Testing Requirements ✓
1. Both services start without errors
2. Frontend can successfully call all backend endpoints
3. User authentication works correctly
4. Question flow works end-to-end
5. Logs are written to correct files with correct prefixes
6. Both databases remain functional and separate

---

## Important Notes

### Critical Requirements
- **DO NOT merge databases** - this is absolutely critical
- **DO NOT copy backend logic to frontend** - always call the API
- **DO NOT modify core algorithms** in `geometry_manager.py` - use as-is
- **ALWAYS log with service prefix** - [FRONTEND] or [BACKEND]
- **Keep user management in frontend** - do not move to backend

### Code Organization
- Copy files from original projects, don't rewrite from scratch
- Preserve existing functionality while adding integration layer
- Keep separation of concerns clear
- Document any deviations from original code

### Performance Considerations
- API calls add latency - consider caching strategies
- Session state management between services
- Database connection pooling if needed

---

## Deliverables

1. Complete `project/` directory structure as specified
2. Fully functional backend service with all API endpoints
3. Fully functional frontend service with backend integration
4. Logging system with separate log files
5. Configuration files and environment variable template
6. README.md with setup and usage instructions
7. Test scripts for validation

---

## Getting Started (For AI Agent)

1. Create the project directory structure
2. Copy files from frontend and backend to appropriate locations
3. Implement backend API server with all endpoints
4. Implement frontend backend client
5. Update frontend pages to use backend client
6. Set up logging for both services
7. Create configuration files
8. Test the integration
9. Write documentation

Good luck! 🚀
