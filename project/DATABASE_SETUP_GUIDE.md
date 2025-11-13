# Database Setup Guide - SQL Server Integration

## 🔄 Database Creation Strategy

**Answer to your question: "Do you create the db each time as in the original backend?"**

**No, with SQL Server the approach is different:**

### 🔍 Original Backend (SQLite):
- ✅ **Automatic Creation**: SQLite files created automatically when accessed
- ✅ **Schema Scripts**: `create.py` and `create_sessions.db.py` created table schemas
- ✅ **File-based**: Database was just a file (`geometry_learning.db`, `sessions.db`)

### 🔄 New Backend (SQL Server):
- ❌ **No Automatic Creation**: SQL Server database must exist on the server first
- ✅ **Auto Table Creation**: Tables are created automatically when app starts
- ✅ **Server-based**: Database lives on SQL Server instance

## 🗄️ Database Setup Process

### **Step 1: Create Database (One-time setup)**
You need to create the database `AKINTOR` on your SQL Server instance first:

```sql
-- Connect to SQL Server Management Studio or Azure Data Studio
-- Run this once:

CREATE DATABASE AKINTOR;
GO

USE AKINTOR;
GO
```

### **Step 2: Automatic Table Creation**
The backend service will automatically:

1. **Check Connection** - Test if it can connect to `AKINTOR` database
2. **Check Tables** - See if required tables exist
3. **Create Tables** - If missing, create all needed tables automatically
4. **Start Service** - Begin accepting API requests

### **Step 3: Verification**

**Manual Table Creation (if needed):**
```powershell
cd backend_service
python create_tables.py
```

**Test Database Setup:**
```powershell
cd backend_service  
python db_utils.py
```

## 📋 Tables Created Automatically

When the backend service starts, it creates these tables if they don't exist:

### **Geometry Learning Tables:**
1. **`Triangles`** - Triangle types (General, Equilateral, Isosceles, Right-angled)
2. **`Theorems`** - Geometric theorems and rules  
3. **`Questions`** - Learning questions with difficulty levels
4. **`TheoremTriangleMatrix`** - Relationships between theorems and triangle types
5. **`TheoremQuestionMatrix`** - Relationships between theorems and questions
6. **`InitialAnswerMultipliers`** - Answer scoring multipliers
7. **`inputDuring`** - User answers during sessions
8. **`inputFB`** - User feedback responses
9. **`QuestionPrerequisites`** - Question dependencies

### **Session Management Table:**
10. **`sessions`** - Session data storage

## 🔧 Configuration Files

### **Database Config:** `backend_service/db_config.py`
```python
DB_CONFIG = {
    'driver': 'SQL Server',
    'server': 'DESKTOP-824DEOL\\SQLEXPRESS01',
    'database': 'AKINTOR',
    'trusted_connection': 'yes'
}
```

### **App Config:** `backend_service/config.py`  
```python
class Config:
    # Database Configuration - SQL Server
    DB_CONFIG = {
        'driver': os.environ.get('DB_DRIVER', 'SQL Server'),
        'server': os.environ.get('DB_SERVER', 'DESKTOP-824DEOL\\SQLEXPRESS01'),
        'database': os.environ.get('DB_DATABASE', 'AKINTOR'),
        'trusted_connection': os.environ.get('DB_TRUSTED_CONNECTION', 'yes')
    }
```

## 🚀 Startup Process

### **When you run `python app.py`:**

1. **🔗 Connection Test**
   ```
   [2025-11-13 10:30:15] [BACKEND] [INFO] - Checking database connection and tables...
   ```

2. **📊 Table Check**
   ```
   [2025-11-13 10:30:16] [BACKEND] [INFO] - Missing tables detected: ['Triangles', 'Questions']
   ```

3. **🏗️ Automatic Creation**
   ```
   [2025-11-13 10:30:17] [BACKEND] [INFO] - Creating database tables...
   [2025-11-13 10:30:18] [BACKEND] [INFO] - ✅ Database tables created successfully!
   ```

4. **🌐 Service Start**
   ```
   [2025-11-13 10:30:19] [BACKEND] [INFO] - Starting backend service on 0.0.0.0:5001
   * Running on http://0.0.0.0:5001
   ```

## 🔄 Key Differences from Original

| Aspect | Original (SQLite) | New (SQL Server) |
|--------|------------------|------------------|
| **Database Creation** | Automatic file creation | Manual database creation required |
| **Table Creation** | Manual script execution | Automatic on app start |
| **Connection** | File path | Server connection string |
| **Data Types** | SQLite types | SQL Server types (NVARCHAR, INT, etc.) |
| **Manager Class** | `GeometryManager` | `SqlGeometryManager` |

## 🛠️ Migration Commands

### **Create Database (SQL Server):**
```sql
-- In SSMS or Azure Data Studio
CREATE DATABASE AKINTOR;
```

### **Reset All Tables:**
```powershell
cd backend_service
python -c "from create_tables import drop_all_tables; drop_all_tables()"
python create_tables.py
```

### **Check Current Status:**
```powershell
cd backend_service
python -c "from create_tables import check_tables_exist; print(check_tables_exist())"
```

## ✅ Quick Setup Checklist

- [ ] SQL Server is running (`DESKTOP-824DEOL\SQLEXPRESS01`)
- [ ] Database `AKINTOR` exists on the server
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend service can connect (`python db_utils.py`)
- [ ] Tables are created automatically when app starts
- [ ] Frontend can call backend API endpoints

## 🎯 Summary

**The new system does NOT create the database each time**, but it DOES:

1. ✅ **Check** if database connection works
2. ✅ **Verify** required tables exist  
3. ✅ **Create** missing tables automatically
4. ✅ **Start** the service ready for requests

This provides a robust setup that's more production-ready than the original SQLite approach while maintaining the same functionality!