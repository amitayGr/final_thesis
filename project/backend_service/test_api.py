"""
Backend API Test Script
Tests the backend service endpoints to ensure they work correctly
"""

import requests
import json

BASE_URL = "http://localhost:5001"


def print_response(title, response):
    """Pretty print response"""
    print(f"\n{'=' * 60}")
    print(f"🔹 {title}")
    print(f"{'=' * 60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response Text: {response.text}")


def test_health():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_session_flow():
    """Test complete session flow"""
    print("\n\n📚 Testing Complete Session Flow...")
    
    # 1. Start session
    print("\n1️⃣ Starting session...")
    response = requests.get(f"{BASE_URL}/api/start")
    print_response("Start Session", response)
    
    if response.status_code != 200:
        print("❌ Failed to start session")
        return False
    
    # Store session cookie
    session = requests.Session()
    session.cookies.update(response.cookies)
    
    # 2. Get first question
    print("\n2️⃣ Getting first question...")
    response = session.get(f"{BASE_URL}/api/question/first")
    print_response("First Question", response)
    
    if response.status_code != 200:
        print("❌ Failed to get first question")
        return False
    
    question_data = response.json()
    question_id = question_data.get('question_id')
    
    # 3. Get available answers
    print("\n3️⃣ Getting available answers...")
    response = session.get(f"{BASE_URL}/api/answers")
    print_response("Available Answers", response)
    
    # 4. Process answer
    print("\n4️⃣ Processing answer...")
    response = session.post(
        f"{BASE_URL}/api/answer",
        json={"question_id": question_id, "answer_id": 1}
    )
    print_response("Process Answer", response)
    
    if response.status_code != 200:
        print("❌ Failed to process answer")
        return False
    
    # 5. Get theorems
    print("\n5️⃣ Getting relevant theorems...")
    response = session.get(
        f"{BASE_URL}/api/theorems",
        params={"question_id": question_id, "answer_id": 1}
    )
    print_response("Relevant Theorems", response)
    
    # 6. Get next question
    print("\n6️⃣ Getting next question...")
    response = session.get(f"{BASE_URL}/api/question/next")
    print_response("Next Question", response)
    
    if response.status_code != 200:
        print("❌ Failed to get next question")
        return False
    
    next_question = response.json()
    next_question_id = next_question.get('question_id')
    
    # 7. Process another answer
    print("\n7️⃣ Processing another answer...")
    response = session.post(
        f"{BASE_URL}/api/answer",
        json={"question_id": next_question_id, "answer_id": 0}
    )
    print_response("Process Second Answer", response)
    
    # 8. Get session state
    print("\n8️⃣ Getting session state...")
    response = session.get(f"{BASE_URL}/api/session/state")
    print_response("Session State", response)
    
    # 9. End session
    print("\n9️⃣ Ending session with feedback...")
    response = session.post(
        f"{BASE_URL}/api/session/end",
        json={
            "feedback_id": 5,
            "triangle_types": [2, 3],
            "helpful_theorems": [15, 23]
        }
    )
    print_response("End Session", response)
    
    return response.status_code == 200


def test_error_handling():
    """Test error handling"""
    print("\n\n⚠️ Testing Error Handling...")
    
    # Test getting question without session
    print("\n1️⃣ Testing request without session...")
    response = requests.get(f"{BASE_URL}/api/question/first")
    print_response("No Session Error", response)
    
    # Test invalid endpoint
    print("\n2️⃣ Testing invalid endpoint...")
    response = requests.get(f"{BASE_URL}/api/invalid")
    print_response("404 Error", response)


def main():
    """Run all tests"""
    print("🚀 Backend API Test Suite")
    print("=" * 60)
    
    try:
        # Test health
        health_ok = test_health()
        if not health_ok:
            print("\n❌ Health check failed. Is the backend service running?")
            return
        
        # Test session flow
        session_ok = test_session_flow()
        if session_ok:
            print("\n✅ Session flow test PASSED")
        else:
            print("\n❌ Session flow test FAILED")
        
        # Test error handling
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("🏁 Test suite completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to backend service!")
        print(f"Make sure the backend is running at {BASE_URL}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
