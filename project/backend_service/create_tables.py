"""
create_tables.py
--------------
Description:
   Create SQL Server tables for the geometry learning system.
   Converts SQLite schema from original backend to SQL Server.

Author: Integration Service
Date: November 2025
"""

from db_utils import execute_query, test_connection
import logging

logger = logging.getLogger('backend_service')


def create_geometry_tables():
    """Create all tables for the geometry learning system in SQL Server"""
    
    if not test_connection():
        logger.error("Cannot connect to database. Please check your SQL Server configuration.")
        return False
    
    try:
        # Enable foreign key constraints (SQL Server equivalent)
        logger.info("Creating Triangles table...")
        execute_query("""
        CREATE TABLE Triangles (
            triangle_id INT PRIMARY KEY,
            triangle_type NVARCHAR(50) NOT NULL,
            active INT DEFAULT 1
        )
        """, fetch=False)
        
        logger.info("Creating Theorems table...")
        execute_query("""
        CREATE TABLE Theorems (
            theorem_id INT IDENTITY(1,1) PRIMARY KEY,
            theorem_text NVARCHAR(MAX) NOT NULL,
            category INT,
            active INT DEFAULT 1,
            FOREIGN KEY (category) REFERENCES Triangles(triangle_id)
        )
        """, fetch=False)
        
        logger.info("Creating Questions table...")
        execute_query("""
        CREATE TABLE Questions (
            question_id INT IDENTITY(1,1) PRIMARY KEY,
            question_text NVARCHAR(MAX) NOT NULL,
            difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 3),
            active INT DEFAULT 1
        )
        """, fetch=False)
        
        logger.info("Creating TheoremTriangleMatrix table...")
        execute_query("""
        CREATE TABLE TheoremTriangleMatrix (
            theorem_id INT,
            triangle_id INT,
            connection_strength FLOAT CHECK (connection_strength >= 0 AND connection_strength <= 1),
            PRIMARY KEY (theorem_id, triangle_id),
            FOREIGN KEY (theorem_id) REFERENCES Theorems(theorem_id),
            FOREIGN KEY (triangle_id) REFERENCES Triangles(triangle_id)
        )
        """, fetch=False)
        
        logger.info("Creating TheoremQuestionMatrix table...")
        execute_query("""
        CREATE TABLE TheoremQuestionMatrix (
            theorem_id INT,
            question_id INT,
            PRIMARY KEY (theorem_id, question_id),
            FOREIGN KEY (theorem_id) REFERENCES Theorems(theorem_id),
            FOREIGN KEY (question_id) REFERENCES Questions(question_id)
        )
        """, fetch=False)
        
        logger.info("Creating InitialAnswerMultipliers table...")
        execute_query("""
        CREATE TABLE InitialAnswerMultipliers (
            question_id INT,
            triangle_id INT,
            answer_type NVARCHAR(50) NOT NULL,
            multiplier REAL NOT NULL,
            PRIMARY KEY (question_id, triangle_id, answer_type),
            FOREIGN KEY (question_id) REFERENCES Questions(question_id),
            FOREIGN KEY (triangle_id) REFERENCES Triangles(triangle_id)
        )
        """, fetch=False)
        
        logger.info("Creating inputDuring table...")
        execute_query("""
        CREATE TABLE inputDuring (
            ansID INT IDENTITY(1,1) PRIMARY KEY,
            ans NVARCHAR(MAX) NOT NULL
        )
        """, fetch=False)
        
        logger.info("Creating inputFB table...")
        execute_query("""
        CREATE TABLE inputFB (
            fbID INT IDENTITY(1,1) PRIMARY KEY,
            fb NVARCHAR(MAX) NOT NULL
        )
        """, fetch=False)
        
        logger.info("Creating QuestionPrerequisites table...")
        execute_query("""
        CREATE TABLE QuestionPrerequisites (
            id INT IDENTITY(1,1) PRIMARY KEY,
            prerequisite_question_id INT,
            dependent_question_id INT,
            FOREIGN KEY (prerequisite_question_id) REFERENCES Questions(question_id),
            FOREIGN KEY (dependent_question_id) REFERENCES Questions(question_id)
        )
        """, fetch=False)
        
        logger.info("✅ All geometry learning tables created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {str(e)}")
        return False


def create_sessions_table():
    """Create sessions table for session management"""
    try:
        logger.info("Creating sessions table...")
        execute_query("""
        CREATE TABLE sessions (
            id INT IDENTITY(1,1) PRIMARY KEY,
            session_id NVARCHAR(255) UNIQUE,
            data NVARCHAR(MAX)
        )
        """, fetch=False)
        
        logger.info("✅ Sessions table created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating sessions table: {str(e)}")
        return False


def drop_all_tables():
    """Drop all tables (for testing/reset purposes)"""
    try:
        logger.warning("Dropping all tables...")
        
        # Drop tables in reverse order due to foreign key constraints
        tables = [
            'QuestionPrerequisites',
            'inputFB', 
            'inputDuring',
            'InitialAnswerMultipliers',
            'TheoremQuestionMatrix',
            'TheoremTriangleMatrix',
            'Questions',
            'Theorems',
            'Triangles',
            'sessions'
        ]
        
        for table in tables:
            try:
                execute_query(f"DROP TABLE IF EXISTS {table}", fetch=False)
                logger.info(f"Dropped table: {table}")
            except Exception as e:
                logger.warning(f"Could not drop table {table}: {e}")
        
        logger.info("✅ All tables dropped successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error dropping tables: {str(e)}")
        return False


def check_tables_exist():
    """Check which tables exist in the database"""
    try:
        results = execute_query("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """)
        
        tables = [row['TABLE_NAME'] for row in results]
        logger.info(f"Existing tables: {tables}")
        return tables
        
    except Exception as e:
        logger.error(f"❌ Error checking tables: {str(e)}")
        return []


if __name__ == "__main__":
    # Setup basic logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [BACKEND] [%(levelname)s] - %(message)s'
    )
    
    print("🔄 SQL Server Database Initialization")
    print("=" * 50)
    
    # Check connection
    print("\n1️⃣ Testing database connection...")
    if not test_connection():
        print("❌ Connection failed! Check your SQL Server configuration.")
        exit(1)
    
    print("✅ Connection successful!")
    
    # Check existing tables
    print("\n2️⃣ Checking existing tables...")
    existing_tables = check_tables_exist()
    
    if existing_tables:
        print(f"Found {len(existing_tables)} existing tables:")
        for table in existing_tables:
            print(f"  • {table}")
        
        response = input("\nDo you want to recreate all tables? (y/N): ").lower()
        if response == 'y':
            print("\n3️⃣ Dropping existing tables...")
            drop_all_tables()
    
    # Create tables
    print("\n4️⃣ Creating geometry learning tables...")
    geometry_success = create_geometry_tables()
    
    print("\n5️⃣ Creating sessions table...")
    sessions_success = create_sessions_table()
    
    # Final check
    print("\n6️⃣ Final verification...")
    final_tables = check_tables_exist()
    
    print(f"\n🎯 Database setup complete!")
    print(f"📊 Tables created: {len(final_tables)}")
    print(f"✅ Geometry tables: {'✓' if geometry_success else '✗'}")
    print(f"✅ Sessions table: {'✓' if sessions_success else '✗'}")
    
    if len(final_tables) >= 9:  # Expected minimum tables
        print("\n🎉 Database is ready for use!")
    else:
        print("\n⚠️ Some tables may be missing. Check the logs above.")