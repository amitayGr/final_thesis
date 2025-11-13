"""
sql_geometry_manager.py
-----------------
Description:
   SQL Server-compatible version of GeometryManager.
   Replaces SQLite-specific code with SQL Server operations.

Author: Integration Service  
Date: November 2025
"""

import pyodbc
from typing import List, Dict
import os
from session import Session
from session_db import SessionDB
from collections import defaultdict
from db_utils import execute_query, get_db_connection
import logging

logger = logging.getLogger('backend_service')


class SqlGeometryManager:
    def __init__(self):
        """Initialize SQL Server-based GeometryManager"""
        self.state = self._initialize_state()
        self.session = Session()
        self.session_db = SessionDB()
        # ===== Back-to-exercise support =====
        self._pending_question = None  # תשמר כאן השאלה האחרונה שהוצגה למשתמש ועדיין ממתינה לתשובה
        self._resume_requested = False  # דגל: האם המשתמש ביקש "חזרה לתרגיל"

    def close(self):
        """Close any open resources (SQL Server connections are handled by db_utils)"""
        pass

    def _initialize_state(self) -> Dict:
        """אתחול מצב פנימי - משקלים התחלתיים וכו'"""
        return {
            'triangle_weights': {
                0: 0.25,  # כללי
                1: 0.25,  # שווה צלעות
                2: 0.25,  # שווה שוקיים
                3: 0.25   # ישר זווית
            },
            'theorem_weights': self._initialize_theorem_weights(),
            'asked_questions': [],
            'questions_count': 0,
        }

    def _initialize_theorem_weights(self) -> Dict[int, float]:
        """Initialize all active theorems with minimal base weight."""
        try:
            results = execute_query("SELECT theorem_id FROM Theorems WHERE active = 1")
            return {row['theorem_id']: 0.01 for row in results}
        except Exception as e:
            logger.error(f"Error initializing theorem weights: {e}")
            return {}

    def get_first_question(self) -> Dict:
        """בחר שאלה ראשונה מתוך שאלות קלות ועדכן את ההיסטוריה."""
        try:
            results = execute_query("""
                SELECT question_id, question_text 
                FROM Questions 
                WHERE active = 1 AND difficulty_level = 1
            """)
            
            easy_questions = results
            if not easy_questions:
                return {"error": "No easy questions found"}

            # הגדרת קווים אם עדיין לא נעשה
            import random
            if not hasattr(self.session, 'target_triangles'):
                self.session.target_triangles = random.sample([0, 1, 2, 3], 2)

            # בחר שאלה באופן רנדומלי
            selected_question = random.choice(easy_questions)
            
            # עדכן היסטוריה
            self.state['asked_questions'].append(selected_question['question_id'])
            self.state['questions_count'] += 1
            
            # שמור כשאלה ממתינה
            self._pending_question = {
                'question_id': selected_question['question_id'],
                'question_text': selected_question['question_text'],
                'difficulty_level': 1
            }
            
            logger.info(f"Selected first question: {selected_question['question_id']}")
            
            return {
                'question_id': selected_question['question_id'],
                'question_text': selected_question['question_text'],
                'difficulty_level': 1
            }
            
        except Exception as e:
            logger.error(f"Error getting first question: {e}")
            return {"error": f"Database error: {str(e)}"}

    def process_answer(self, user_answer: str, question_id: int) -> Dict:
        """עיבוד תשובת המשתמש והחזרת השאלה הבאה."""
        try:
            # שמור תשובה במסד הנתונים
            execute_query(
                "INSERT INTO inputDuring (ans) VALUES (?)", 
                (user_answer,), 
                fetch=False
            )
            
            # עדכן משקלים בהתבסס על התשובה
            self._update_weights_based_on_answer(user_answer, question_id)
            
            # בחר שאלה הבאה
            next_question = self._select_next_question()
            
            if next_question:
                self._pending_question = next_question
                self.state['asked_questions'].append(next_question['question_id'])
                self.state['questions_count'] += 1
                
                logger.info(f"Selected next question: {next_question['question_id']}")
            
            return next_question
            
        except Exception as e:
            logger.error(f"Error processing answer: {e}")
            return {"error": f"Processing error: {str(e)}"}

    def _update_weights_based_on_answer(self, user_answer: str, question_id: int):
        """עדכון משקלים בהתבסס על תשובת המשתמש."""
        try:
            # Get theorems related to this question
            related_theorems = execute_query("""
                SELECT tq.theorem_id, t.theorem_text
                FROM TheoremQuestionMatrix tq
                JOIN Theorems t ON tq.theorem_id = t.theorem_id
                WHERE tq.question_id = ? AND t.active = 1
            """, (question_id,))
            
            # Simple logic: if answer contains theorem keywords, boost that theorem
            user_answer_lower = user_answer.lower()
            
            for theorem in related_theorems:
                theorem_id = theorem['theorem_id']
                theorem_text = theorem['theorem_text'].lower()
                
                # Check if user mentioned this theorem
                theorem_keywords = theorem_text.split()[:3]  # First 3 words as keywords
                
                mentioned = any(keyword.lower() in user_answer_lower for keyword in theorem_keywords if len(keyword) > 2)
                
                if mentioned:
                    # Boost this theorem's weight
                    current_weight = self.state['theorem_weights'].get(theorem_id, 0.01)
                    self.state['theorem_weights'][theorem_id] = min(current_weight * 1.5, 1.0)
                    logger.info(f"Boosted theorem {theorem_id} weight to {self.state['theorem_weights'][theorem_id]}")
                
        except Exception as e:
            logger.error(f"Error updating weights: {e}")

    def _select_next_question(self) -> Dict:
        """בחירת השאלה הבאה באמצעות אלגוריתם האנטרופיה."""
        try:
            # Get all available questions not yet asked
            asked_questions_str = ','.join(map(str, self.state['asked_questions'])) if self.state['asked_questions'] else '0'
            
            available_questions = execute_query(f"""
                SELECT question_id, question_text, difficulty_level
                FROM Questions 
                WHERE active = 1 AND question_id NOT IN ({asked_questions_str})
            """)
            
            if not available_questions:
                return {"message": "No more questions available"}
            
            # Simple selection: prefer questions with higher difficulty or related to target theorems
            best_question = None
            best_score = -1
            
            for question in available_questions:
                # Check if this question relates to our high-weight theorems
                related_theorems = execute_query("""
                    SELECT theorem_id
                    FROM TheoremQuestionMatrix 
                    WHERE question_id = ?
                """, (question['question_id'],))
                
                score = question['difficulty_level']  # Base score from difficulty
                
                # Add bonus for theorems we want to focus on
                for theorem_rel in related_theorems:
                    theorem_id = theorem_rel['theorem_id']
                    theorem_weight = self.state['theorem_weights'].get(theorem_id, 0.01)
                    score += theorem_weight * 10  # Scale weight impact
                
                if score > best_score:
                    best_score = score
                    best_question = question
            
            if best_question:
                return {
                    'question_id': best_question['question_id'],
                    'question_text': best_question['question_text'],
                    'difficulty_level': best_question['difficulty_level']
                }
            else:
                # Fallback to first available question
                return available_questions[0]
                
        except Exception as e:
            logger.error(f"Error selecting next question: {e}")
            return {"error": f"Selection error: {str(e)}"}

    def get_current_question(self) -> Dict:
        """החזרת השאלה הנוכחית הממתינה לתשובה."""
        if self._pending_question:
            return self._pending_question
        else:
            return {"error": "No current question"}

    def reset_session(self):
        """איפוס סשן - התחלה מחדש."""
        self.state = self._initialize_state()
        self.session = Session()
        self._pending_question = None
        self._resume_requested = False
        logger.info("Session reset completed")

    def get_feedback_questions(self) -> List[Dict]:
        """החזרת שאלות פידבק."""
        return [
            {"id": 1, "text": "האם התרגילים עזרו לך להבין טוב יותר את המשולשים?"},
            {"id": 2, "text": "איזה סוג משולש הכי קשה לך?"},
            {"id": 3, "text": "האם המשפטים שהוצגו היו ברורים?"},
            {"id": 4, "text": "מה לדעתך חסר במערכת?"},
            {"id": 5, "text": "האם תרצה להמשיך ללמוד?"},
            {"id": 6, "text": "עד כמה אתה מרוצה מהחוויה? (1-5)"},
            {"id": 7, "text": "האם תרצה לחזור לתרגיל?"}
        ]

    # Additional helper methods for compatibility with original API...
    
    def get_statistics(self) -> Dict:
        """Get session statistics"""
        return {
            'questions_answered': len(self.state['asked_questions']),
            'current_triangle_weights': self.state['triangle_weights'],
            'current_theorem_weights': dict(list(self.state['theorem_weights'].items())[:10])  # Top 10
        }
        
    def get_session_data(self) -> Dict:
        """Get current session data"""
        return {
            'session_id': getattr(self.session, 'session_id', None),
            'questions_count': self.state['questions_count'],
            'asked_questions': self.state['asked_questions']
        }