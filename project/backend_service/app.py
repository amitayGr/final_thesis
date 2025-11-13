from flask import Flask, session, jsonify, request
from flask_cors import CORS
from sql_geometry_manager import SqlGeometryManager
from config import Config, setup_logging
import traceback

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS for frontend requests

# Setup logging
logger = setup_logging()
logger.info("Backend service starting...")

# Store SqlGeometryManager instances per session
# In production, consider using Redis or similar for distributed sessions
geometry_managers = {}


def get_manager():
    """Get or create SqlGeometryManager for current session"""
    session_id = session.get('session_id')
    if not session_id or session_id not in geometry_managers:
        logger.error(f"No geometry manager found for session: {session_id}")
        return None
    return geometry_managers[session_id]


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({
        "status": "healthy",
        "service": "backend_geometry_learning",
        "version": "1.0.0"
    }), 200


@app.route('/api/start', methods=['GET'])
def start_session():
    """Initialize a new learning session"""
    try:
        # Create new SqlGeometryManager instance
        manager = SqlGeometryManager()
        
        # Generate session ID and store manager
        import uuid
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        geometry_managers[session_id] = manager
        
        logger.info(f"Session initialized: session_id={session_id}")
        
        return jsonify({
            "message": "Session initialized successfully",
            "session_id": session_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error starting session: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to initialize session",
            "message": str(e)
        }), 500


@app.route('/api/question/first', methods=['GET'])
def get_first_question():
    """Get the first question for the session"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        question = manager.get_first_question()
        
        if "error" in question:
            logger.warning(f"No first question found: {question['error']}")
            return jsonify(question), 404
        
        logger.info(f"First question selected: question_id={question['question_id']}")
        
        return jsonify(question), 200
        
    except Exception as e:
        logger.error(f"Error getting first question: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to get first question",
            "message": str(e)
        }), 500


@app.route('/api/question/next', methods=['GET'])
def get_next_question():
    """Get the next question based on current session state"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        # Check if resume was requested
        if manager._resume_requested and manager._pending_question:
            question = manager._pending_question
            manager._resume_requested = False
            logger.info(f"Resuming with pending question: question_id={question.get('question_id')}")
        else:
            question = manager.get_next_question()
            manager._store_pending_question(question)
            
            if "error" in question:
                logger.warning(f"No next question available: {question['error']}")
                return jsonify(question), 404
            
            logger.info(f"Next question selected: question_id={question['question_id']}, method={question.get('info', 'N/A')}")
        
        return jsonify(question), 200
        
    except Exception as e:
        logger.error(f"Error getting next question: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to get next question",
            "message": str(e)
        }), 500


@app.route('/api/answer', methods=['POST'])
def process_answer():
    """Process student answer and update weights"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        data = request.get_json()
        if not data or 'question_id' not in data or 'answer_id' not in data:
            return jsonify({
                "error": "Invalid request",
                "message": "question_id and answer_id are required"
            }), 400
        
        question_id = data['question_id']
        answer_id = data['answer_id']
        
        logger.info(f"Processing answer: question_id={question_id}, answer_id={answer_id}")
        
        # Process the answer (this updates weights internally)
        manager.process_answer(question_id, answer_id)
        
        # Get updated state
        triangle_weights = manager.state['triangle_weights']
        
        logger.info(f"Answer processed successfully. Updated triangle weights: {triangle_weights}")
        
        return jsonify({
            "message": "Answer processed successfully",
            "triangle_weights": triangle_weights
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing answer: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to process answer",
            "message": str(e)
        }), 500


@app.route('/api/theorems', methods=['GET'])
def get_theorems():
    """Get relevant theorem recommendations"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        # Get query parameters
        question_id = request.args.get('question_id', type=int)
        answer_id = request.args.get('answer_id', type=int)
        base_threshold = request.args.get('base_threshold', default=0.01, type=float)
        
        if question_id is None or answer_id is None:
            return jsonify({
                "error": "Invalid request",
                "message": "question_id and answer_id are required as query parameters"
            }), 400
        
        logger.info(f"Getting theorems: question_id={question_id}, answer_id={answer_id}")
        
        theorems = manager.get_relevant_theorems(question_id, answer_id, base_threshold)
        
        logger.info(f"Retrieved {len(theorems)} relevant theorems")
        
        return jsonify({
            "theorems": theorems,
            "count": len(theorems)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting theorems: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to get theorems",
            "message": str(e)
        }), 500


@app.route('/api/session/state', methods=['GET'])
def get_session_state():
    """Get current session state (weights, asked questions, etc.)"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        state = {
            "triangle_weights": manager.state['triangle_weights'],
            "asked_questions": manager.state['asked_questions'],
            "questions_count": manager.state['questions_count'],
            "session_data": manager.session.to_dict()
        }
        
        logger.info(f"Session state retrieved: {state['questions_count']} questions asked")
        
        return jsonify(state), 200
        
    except Exception as e:
        logger.error(f"Error getting session state: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to get session state",
            "message": str(e)
        }), 500


@app.route('/api/session/end', methods=['POST'])
def end_session():
    """End session with feedback"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body is required"
            }), 400
        
        feedback_id = data.get('feedback_id')
        triangle_types = data.get('triangle_types', [])
        helpful_theorems = data.get('helpful_theorems', [])
        
        logger.info(f"Ending session: feedback_id={feedback_id}, triangle_types={triangle_types}, helpful_theorems={helpful_theorems}")
        
        # Set feedback and additional data
        if feedback_id is not None:
            manager.session.set_feedback(feedback_id)
        
        if triangle_types:
            manager.session.set_triangle_type(triangle_types)
        
        if helpful_theorems:
            manager.session.set_helpful_theorems(helpful_theorems)
        
        # Check if user wants to resume (feedback_id == 7)
        if feedback_id == 7:
            manager._resume_requested = True
            logger.info("User requested to resume - not saving session")
            return jsonify({
                "message": "Resume requested",
                "action": "resume"
            }), 200
        
        # Save session to database
        manager.session_db.save_session(manager.session)
        session_data = manager.session.to_dict()
        
        # Clean up manager from memory
        session_id = session.get('session_id')
        if session_id in geometry_managers:
            geometry_managers[session_id].close()
            del geometry_managers[session_id]
        
        logger.info(f"Session ended and saved: session_id={session_data['session_id']}")
        
        return jsonify({
            "message": "Session ended successfully",
            "action": "saved",
            "session_data": session_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error ending session: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to end session",
            "message": str(e)
        }), 500


@app.route('/api/answers', methods=['GET'])
def get_available_answers():
    """Get available answer options"""
    try:
        manager = get_manager()
        if not manager:
            return jsonify({"error": "No active session. Please call /api/start first"}), 400
        
        cursor = manager.conn.cursor()
        cursor.execute("SELECT ansID, ans FROM inputDuring")
        answers = [{"answer_id": row[0], "answer_text": row[1]} for row in cursor.fetchall()]
        
        logger.info(f"Retrieved {len(answers)} available answers")
        
        return jsonify({
            "answers": answers,
            "count": len(answers)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting answers: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Failed to get answers",
            "message": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.url}")
    return jsonify({
        "error": "Endpoint not found",
        "message": f"The requested URL {request.url} was not found on this server"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}\n{traceback.format_exc()}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting backend service on {Config.HOST}:{Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info(f"Database config: {Config.DB_CONFIG}")
    
    # Initialize database tables if they don't exist
    try:
        from create_tables import check_tables_exist, create_geometry_tables, create_sessions_table
        from db_utils import test_connection
        
        logger.info("Checking database connection and tables...")
        
        if test_connection():
            existing_tables = check_tables_exist()
            
            # Check if essential tables exist
            required_tables = ['Triangles', 'Questions', 'Theorems']
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                logger.info(f"Missing tables detected: {missing_tables}")
                logger.info("Creating database tables...")
                
                geometry_success = create_geometry_tables()
                sessions_success = create_sessions_table()
                
                if geometry_success and sessions_success:
                    logger.info("✅ Database tables created successfully!")
                else:
                    logger.warning("⚠️ Some tables may not have been created properly")
            else:
                logger.info("✅ All required database tables exist")
        else:
            logger.error("❌ Cannot connect to database. Please check your SQL Server configuration.")
            logger.error("The application will start but database operations will fail.")
            
    except Exception as e:
        logger.error(f"❌ Database initialization error: {str(e)}")
        logger.error("The application will start but database operations may fail.")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
