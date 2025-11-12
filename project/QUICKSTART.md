# Quick Start Guide

## 🚀 Fastest Way to Get Started

### Option 1: Using the Startup Script (Recommended)

1. Open PowerShell in the project directory:
   ```powershell
   cd c:\Users\lahavor\am\final_thesis\project
   ```

2. Run the startup script:
   ```powershell
   .\start.ps1
   ```

3. The script will:
   - ✅ Start backend service (port 5001)
   - ✅ Start frontend service (port 5000)
   - ✅ Open your browser automatically

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```powershell
cd c:\Users\lahavor\am\final_thesis\project\backend_service
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\lahavor\am\final_thesis\project\frontend_service
pip install -r requirements.txt
python app.py
```

**Then open browser:**
- Frontend: http://localhost:5000

---

## ✅ Verify Everything Works

### 1. Check Backend Health

Open browser to: http://localhost:5001/api/health

You should see:
```json
{
  "status": "healthy",
  "service": "backend_geometry_learning",
  "version": "1.0.0"
}
```

### 2. Test Backend API

```powershell
cd backend_service
python test_api.py
```

You should see all tests passing.

### 3. Check Frontend

Open: http://localhost:5000

You should see the home page.

---

## 📊 Check Logs

Logs are written to:
- `logs/backend_service.log`
- `logs/frontend_service.log`

View logs in real-time:
```powershell
# Backend logs
Get-Content logs\backend_service.log -Wait -Tail 20

# Frontend logs
Get-Content logs\frontend_service.log -Wait -Tail 20
```

---

## 🛑 Stopping the Services

### If using start.ps1:
Close both PowerShell windows that opened

### If manual start:
Press `Ctrl+C` in each terminal

---

## ⚠️ Common Issues

### "Port already in use"
```powershell
# Find and kill process on port 5001
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Module not found"
```powershell
# Install dependencies
cd backend_service
pip install -r requirements.txt

cd ..\frontend_service
pip install -r requirements.txt
```

### "Cannot connect to backend"
1. Make sure backend is running (check port 5001)
2. Check `logs/backend_service.log` for errors
3. Try: http://localhost:5001/api/health

---

## 🎯 Next Steps

1. ✅ Register a new user
2. ✅ Login
3. ✅ Navigate to Question page
4. ✅ Answer questions and see adaptive learning in action
5. ✅ Check logs to see [FRONTEND] and [BACKEND] prefixes

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Need Help?**
- Check logs in `logs/` directory
- Run `python test_api.py` in backend_service
- See [README.md](README.md) troubleshooting section
