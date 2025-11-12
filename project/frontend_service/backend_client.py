import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("frontend_service")


class BackendClient:
    """Client for communicating with the backend geometry learning service"""
    
    def __init__(self, base_url: str = "http://localhost:5001", timeout: int = 30):
        """
        Initialize the backend client
        
        Args:
            base_url: Base URL of the backend service
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        logger.info(f"[FRONTEND] BackendClient initialized with base_url={self.base_url}")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make an HTTP request to the backend service
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data as dictionary or error dict
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"[FRONTEND] Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            logger.info(f"[FRONTEND] Backend response: status={response.status_code}")
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError:
                data = {"text": response.text}
            
            if response.status_code >= 400:
                logger.error(f"[FRONTEND] Backend error: {data}")
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": data.get("message", data.get("error", "Unknown error")),
                    "data": data
                }
            
            logger.info(f"[FRONTEND] Backend request successful")
            return {
                "error": False,
                "status_code": response.status_code,
                "data": data
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"[FRONTEND] Backend request timeout for {url}")
            return {
                "error": True,
                "message": "Backend service timeout - request took too long",
                "timeout": True
            }
            
        except requests.exceptions.ConnectionError:
            logger.error(f"[FRONTEND] Cannot connect to backend service at {url}")
            return {
                "error": True,
                "message": "Cannot connect to backend service - service may be down",
                "connection_error": True
            }
            
        except Exception as e:
            logger.error(f"[FRONTEND] Unexpected error calling backend: {str(e)}")
            return {
                "error": True,
                "message": f"Unexpected error: {str(e)}"
            }
    
    def health_check(self) -> Dict:
        """
        Check if backend service is healthy
        
        Returns:
            Health status dictionary
        """
        logger.info("[FRONTEND] Checking backend health")
        return self._make_request("GET", "/api/health")
    
    def start_session(self) -> Dict:
        """
        Initialize a new learning session
        
        Returns:
            Session initialization response
        """
        logger.info("[FRONTEND] Starting new backend session")
        return self._make_request("GET", "/api/start")
    
    def get_first_question(self) -> Dict:
        """
        Get the first question for a new session
        
        Returns:
            First question data
        """
        logger.info("[FRONTEND] Requesting first question")
        return self._make_request("GET", "/api/question/first")
    
    def get_next_question(self) -> Dict:
        """
        Get the next question based on current state
        
        Returns:
            Next question data
        """
        logger.info("[FRONTEND] Requesting next question")
        return self._make_request("GET", "/api/question/next")
    
    def process_answer(self, question_id: int, answer_id: int) -> Dict:
        """
        Process student answer and update learning state
        
        Args:
            question_id: ID of the question being answered
            answer_id: ID of the selected answer
            
        Returns:
            Processing result with updated weights
        """
        logger.info(f"[FRONTEND] Processing answer: question_id={question_id}, answer_id={answer_id}")
        return self._make_request(
            "POST",
            "/api/answer",
            json={
                "question_id": question_id,
                "answer_id": answer_id
            }
        )
    
    def get_theorems(self, question_id: int, answer_id: int, base_threshold: float = 0.01) -> Dict:
        """
        Get relevant theorem recommendations
        
        Args:
            question_id: ID of the question
            answer_id: ID of the answer
            base_threshold: Minimum threshold for theorem relevance
            
        Returns:
            List of relevant theorems
        """
        logger.info(f"[FRONTEND] Requesting theorems: question_id={question_id}, answer_id={answer_id}")
        return self._make_request(
            "GET",
            "/api/theorems",
            params={
                "question_id": question_id,
                "answer_id": answer_id,
                "base_threshold": base_threshold
            }
        )
    
    def get_session_state(self) -> Dict:
        """
        Get current session state (weights, asked questions, etc.)
        
        Returns:
            Current session state
        """
        logger.info("[FRONTEND] Requesting session state")
        return self._make_request("GET", "/api/session/state")
    
    def end_session(self, feedback_id: Optional[int] = None, 
                   triangle_types: Optional[List[int]] = None,
                   helpful_theorems: Optional[List[int]] = None) -> Dict:
        """
        End the current session with feedback
        
        Args:
            feedback_id: User feedback ID (4-7)
            triangle_types: List of triangle type IDs that were relevant
            helpful_theorems: List of theorem IDs that were helpful
            
        Returns:
            Session end result
        """
        logger.info(f"[FRONTEND] Ending session: feedback_id={feedback_id}")
        
        payload = {}
        if feedback_id is not None:
            payload['feedback_id'] = feedback_id
        if triangle_types:
            payload['triangle_types'] = triangle_types
        if helpful_theorems:
            payload['helpful_theorems'] = helpful_theorems
        
        return self._make_request("POST", "/api/session/end", json=payload)
    
    def get_available_answers(self) -> Dict:
        """
        Get available answer options
        
        Returns:
            List of available answers
        """
        logger.info("[FRONTEND] Requesting available answers")
        return self._make_request("GET", "/api/answers")


# Singleton instance
_backend_client_instance = None


def get_backend_client(base_url: str = None) -> BackendClient:
    """
    Get or create singleton BackendClient instance
    
    Args:
        base_url: Backend service URL (only used on first call)
        
    Returns:
        BackendClient instance
    """
    global _backend_client_instance
    
    if _backend_client_instance is None:
        if base_url is None:
            base_url = "http://localhost:5001"
        _backend_client_instance = BackendClient(base_url)
    
    return _backend_client_instance
