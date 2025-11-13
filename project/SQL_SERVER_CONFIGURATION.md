# SQL Server Configuration Guide

## ✅ Configuration Complete!

Your project has been updated to use **SQL Server** instead of SQLite.

## 📋 Database Configuration

### Current Settings:
```python
{
    'driver': 'SQL Server',
    'server': 'DESKTOP-824DEOL\SQLEXPRESS01',
    'database': 'AKINTOR',
    'trusted_connection': 'yes'
}
```

## 🔧 Files Updated

### 1. **Backend Service Configuration**
- **File:** `backend_service/config.py`
- **Change:** Replaced SQLite paths with SQL Server config
- **New:** `DB_CONFIG` dictionary with SQL Server connection parameters

### 2. **Backend Database Config**
- **File:** `backend_service/db_config.py` *(NEW)*
- **Purpose:** Centralized database configuration
- **Features:** Environment variable support, multiple developer configs

### 3. **Backend Database Utilities**
- **File:** `backend_service/db_utils.py` *(NEW)*
- **Purpose:** SQL Server connection helpers
- **Functions:**
  - `get_connection_string()` - Generate ODBC connection string
  - `get_db_connection()` - Create database connection
  - `execute_query()` - Execute queries with parameters
  - `test_connection()` - Test database connectivity

### 4. **Frontend Database Config**
- **File:** `frontend_service/db_config.py`
- **Status:** Already configured (unchanged)
- **Config:** Same SQL Server settings

### 5. **Requirements Files**
- **Files:** `backend_service/requirements.txt`
- **Added:** `pyodbc==5.0.1` for SQL Server connectivity
- **Note:** Frontend already had `pyodbc`

### 6. **Environment Variables**
- **File:** `.env.example`
- **Updated:** Replaced SQLite paths with SQL Server configuration

## 🚀 Setup Instructions

### Step 1: Install ODBC Driver (if not already installed)
```powershell
# Download and install Microsoft ODBC Driver 17 for SQL Server
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### Step 2: Install Python Dependencies
```powershell
cd backend_service
pip install -r requirements.txt

cd ..\frontend_service
pip install -r requirements.txt
```

### Step 3: Test Database Connection
```powershell
cd backend_service
python db_utils.py
```

Expected output:
```
Testing database connection...
Connection String: DRIVER={SQL Server};SERVER=DESKTOP-824DEOL\SQLEXPRESS01;DATABASE=AKINTOR;Trusted_Connection=yes;
✓ Connection successful!

SQL Server Version:
Microsoft SQL Server 2019...
```

### Step 4: Create Environment File (Optional)
```powershell
cd ..
Copy-Item .env.example .env
# Edit .env if you need different settings
```

### Step 5: Update Your Code to Use SQL Server

#### Example: Using db_utils in your code
```python
from db_utils import execute_query, get_db_connection

# Simple query
results = execute_query("SELECT * FROM Users WHERE id = ?", (user_id,))

# Insert/Update
execute_query(
    "INSERT INTO Sessions (user_id, score) VALUES (?, ?)",
    (user_id, score),
    fetch=False
)

# Custom connection handling
connection = get_db_connection()
cursor = connection.cursor()
# ... your code ...
cursor.close()
connection.close()
```

## 🔄 Migrating from SQLite to SQL Server

If you have existing SQLite databases that need to be migrated:

### Option 1: Manual Migration
1. Export SQLite data to CSV
2. Import CSV into SQL Server using SQL Server Management Studio (SSMS)

### Option 2: Using Python Script
```python
import sqlite3
import pyodbc
from db_utils import get_db_connection

# Connect to SQLite
sqlite_conn = sqlite3.connect('geometry_learning.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to SQL Server
sqlserver_conn = get_db_connection()
sqlserver_cursor = sqlserver_conn.cursor()

# Example: Migrate a table
sqlite_cursor.execute("SELECT * FROM Questions")
rows = sqlite_cursor.fetchall()

for row in rows:
    sqlserver_cursor.execute(
        "INSERT INTO Questions VALUES (?, ?, ?, ...)",
        row
    )

sqlserver_conn.commit()
```

## 🔧 Configuration Options

### Using Different SQL Server Instances

#### Option 1: Edit db_config.py directly
```python
DB_CONFIG = {
    'driver': 'SQL Server',
    'server': 'YOUR_SERVER\\INSTANCE_NAME',
    'database': 'YOUR_DATABASE',
    'trusted_connection': 'yes'
}
```

#### Option 2: Use Environment Variables
Create/edit `.env` file:
```env
DB_DRIVER=SQL Server
DB_SERVER=YOUR_SERVER\INSTANCE_NAME
DB_DATABASE=YOUR_DATABASE
DB_TRUSTED_CONNECTION=yes
```

#### Option 3: Use SQL Authentication (instead of Windows Auth)
```python
DB_CONFIG = {
    'driver': 'SQL Server',
    'server': 'YOUR_SERVER\\INSTANCE_NAME',
    'database': 'YOUR_DATABASE',
    'username': 'your_username',
    'password': 'your_password'
}
```

## 📝 Update Your Backend Code

### Before (SQLite):
```python
import sqlite3
conn = sqlite3.connect('geometry_learning.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Questions")
```

### After (SQL Server):
```python
from db_utils import execute_query
results = execute_query("SELECT * FROM Questions")
# results is a list of dictionaries
```

## 🐛 Troubleshooting

### Error: "Data source name not found"
- Install Microsoft ODBC Driver for SQL Server
- Verify driver name: `{SQL Server}` or `{ODBC Driver 17 for SQL Server}`

### Error: "Login failed for user"
- Check Windows authentication is enabled on SQL Server
- Verify SQL Server instance is running
- Check firewall settings

### Error: "Cannot open database"
- Verify database name is correct: `AKINTOR`
- Check user has permissions to access the database
- Verify SQL Server instance: `DESKTOP-824DEOL\SQLEXPRESS01`

### Test Connection:
```powershell
cd backend_service
python -c "from db_utils import test_connection; test_connection()"
```

## 📚 Additional Resources

- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)
- [SQL Server Connection Strings](https://www.connectionstrings.com/sql-server/)
- [Microsoft ODBC Driver Download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

## 🎯 Quick Reference

**Configuration Format:**
```python
{
    'driver': 'SQL Server',
    'server': 'DESKTOP-824DEOL\\SQLEXPRESS01',
    'database': 'AKINTOR',
    'trusted_connection': 'yes'
}
```

**Test Connection:**
```powershell
cd backend_service
python db_utils.py
```

**Use in Code:**
```python
from db_utils import execute_query
results = execute_query("SELECT * FROM TableName")
```

---

This is now your **default configuration** in both backend and frontend services! 🎉