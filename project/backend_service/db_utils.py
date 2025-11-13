"""
db_utils.py
-----------
Description:
   Database utility functions for SQL Server connections.
   Provides helper functions for connecting to and querying SQL Server.

Author: Integration Service
Date: November 2025
"""

import pyodbc
import logging
from db_config import DB_CONFIG

logger = logging.getLogger('backend_service')


def get_connection_string():
    """
    Generate SQL Server connection string from DB_CONFIG.
    
    Returns:
        str: ODBC connection string
    """
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
    )
    
    if DB_CONFIG.get('trusted_connection', '').lower() == 'yes':
        conn_str += "Trusted_Connection=yes;"
    elif 'username' in DB_CONFIG and 'password' in DB_CONFIG:
        conn_str += f"UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']};"
    
    return conn_str


def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
        pyodbc.Connection: Database connection object
        
    Raises:
        pyodbc.Error: If connection fails
    """
    try:
        conn_str = get_connection_string()
        connection = pyodbc.connect(conn_str)
        logger.info(f"Successfully connected to database: {DB_CONFIG['database']}")
        return connection
    except pyodbc.Error as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise


def execute_query(query, params=None, fetch=True):
    """
    Execute a SQL query with optional parameters.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters for parameterized queries
        fetch (bool): Whether to fetch results (SELECT) or just execute (INSERT/UPDATE/DELETE)
        
    Returns:
        list: Query results if fetch=True, otherwise row count
        
    Raises:
        pyodbc.Error: If query execution fails
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            # For SELECT queries
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            logger.info(f"Query executed successfully, returned {len(results)} rows")
            return results
        else:
            # For INSERT/UPDATE/DELETE queries
            connection.commit()
            row_count = cursor.rowcount
            logger.info(f"Query executed successfully, affected {row_count} rows")
            return row_count
            
    except pyodbc.Error as e:
        logger.error(f"Query execution failed: {str(e)}")
        if connection:
            connection.rollback()
        raise
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def test_connection():
    """
    Test the database connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test the connection when run directly
    print("Testing database connection...")
    print(f"Connection String: {get_connection_string()}")
    
    if test_connection():
        print("✓ Connection successful!")
        
        # Try a simple query
        try:
            results = execute_query("SELECT @@VERSION as Version")
            print(f"\nSQL Server Version:")
            print(results[0]['Version'])
        except Exception as e:
            print(f"✗ Query failed: {e}")
    else:
        print("✗ Connection failed!")