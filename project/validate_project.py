"""
Project Integration Validation Script
Checks that all required files and directories are in place
"""

import os
import sys

def check_file_exists(path, description):
    """Check if a file exists and print result"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory_exists(path, description):
    """Check if a directory exists and print result"""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("=" * 70)
    print("🔍 PROJECT INTEGRATION VALIDATION")
    print("=" * 70)
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    all_checks = []
    
    print("\n📁 Directory Structure:")
    all_checks.append(check_directory_exists(
        os.path.join(project_root, "backend_service"),
        "Backend service directory"
    ))
    all_checks.append(check_directory_exists(
        os.path.join(project_root, "frontend_service"),
        "Frontend service directory"
    ))
    all_checks.append(check_directory_exists(
        os.path.join(project_root, "logs"),
        "Logs directory"
    ))
    
    print("\n🔧 Backend Service Files:")
    backend_path = os.path.join(project_root, "backend_service")
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "app.py"),
        "Backend app.py"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "config.py"),
        "Backend config.py"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "geometry_manager.py"),
        "GeometryManager"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "session.py"),
        "Session model"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "session_db.py"),
        "Session database"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "geometry_learning.db"),
        "Geometry learning database"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "sessions.db"),
        "Sessions database"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "requirements.txt"),
        "Backend requirements.txt"
    ))
    all_checks.append(check_file_exists(
        os.path.join(backend_path, "test_api.py"),
        "API test script"
    ))
    
    print("\n🎨 Frontend Service Files:")
    frontend_path = os.path.join(project_root, "frontend_service")
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "app.py"),
        "Frontend app.py"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "config.py"),
        "Frontend config.py"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "backend_client.py"),
        "Backend client"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "auth_config.py"),
        "Auth config"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "db_config.py"),
        "DB config"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "db_utils.py"),
        "DB utils"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "email_utils.py"),
        "Email utils"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "extensions.py"),
        "Extensions"
    ))
    all_checks.append(check_file_exists(
        os.path.join(frontend_path, "requirements.txt"),
        "Frontend requirements.txt"
    ))
    all_checks.append(check_directory_exists(
        os.path.join(frontend_path, "pages"),
        "Pages directory"
    ))
    all_checks.append(check_directory_exists(
        os.path.join(frontend_path, "static"),
        "Static directory"
    ))
    all_checks.append(check_directory_exists(
        os.path.join(frontend_path, "templates"),
        "Templates directory"
    ))
    
    print("\n📄 Documentation Files:")
    all_checks.append(check_file_exists(
        os.path.join(project_root, "README.md"),
        "README.md"
    ))
    all_checks.append(check_file_exists(
        os.path.join(project_root, "QUICKSTART.md"),
        "QUICKSTART.md"
    ))
    all_checks.append(check_file_exists(
        os.path.join(project_root, "INTEGRATION_SUMMARY.md"),
        "INTEGRATION_SUMMARY.md"
    ))
    all_checks.append(check_file_exists(
        os.path.join(project_root, ".env.example"),
        ".env.example"
    ))
    all_checks.append(check_file_exists(
        os.path.join(project_root, "start.ps1"),
        "start.ps1"
    ))
    
    print("\n" + "=" * 70)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100
    
    print(f"📊 VALIDATION RESULTS: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("✅ All checks passed! Project is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: pip install -r backend_service/requirements.txt")
        print("   2. Install dependencies: pip install -r frontend_service/requirements.txt")
        print("   3. Run: .\\start.ps1 (or start manually)")
        print("   4. Open: http://localhost:5000")
        return 0
    else:
        print("❌ Some checks failed. Please review the missing files.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
