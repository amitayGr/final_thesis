# VS Code Configuration - Quick Reference

## 🚀 One-Click Operations

### Start Everything
Press `F5` → Select **"Full Stack (Frontend + Backend)"**

That's it! Both services start with debugging enabled.

---

## ⌨️ Essential Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Start Debugging | `F5` | Launch selected debug config |
| Stop Debugging | `Shift+F5` | Stop all debug sessions |
| Run Task | `Ctrl+Shift+P` → Tasks | Open task list |
| Toggle Terminal | `Ctrl+`` | Show/hide terminal |
| Debug Panel | `Ctrl+Shift+D` | Open debug configurations |
| Extensions | `Ctrl+Shift+X` | Manage extensions |

---

## 📋 Most Used Tasks

Access via: `Ctrl+Shift+P` → "Tasks: Run Task"

1. **Start Both Services** - Launch frontend and backend
2. **Stop All Services** - Kill all Python processes
3. **Run Backend Tests** - Execute test suite
4. **View All Logs** - Real-time log viewing
5. **Install All Dependencies** - Setup project
6. **Open Browser (Frontend)** - Open http://localhost:5000

---

## 🐛 Debug Configurations

Available in Debug panel (`Ctrl+Shift+D`):

- **Full Stack** ⭐ - Both services with debugging
- **Backend Service** - Backend API only
- **Frontend Service** - Frontend only
- **Backend API Tests** - Test suite with debugging

---

## 🧪 API Testing

1. Open `api_tests.http`
2. Click "Send Request" above any request
3. View response in split panel

**Includes:**
- Health checks
- Complete workflows
- Error testing
- All endpoints

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.vscode/launch.json` | Debug configurations |
| `.vscode/tasks.json` | Automated tasks |
| `.vscode/settings.json` | Workspace settings |
| `.vscode/extensions.json` | Recommended extensions |
| `api_tests.http` | API testing file |
| `.vscode/README.md` | Complete documentation |

---

## ✅ First-Time Setup Checklist

- [ ] Open project in VS Code (`code .`)
- [ ] Install recommended extensions (when prompted)
- [ ] Press `Ctrl+Shift+P` → Run task: "Install All Dependencies"
- [ ] Press `F5` → Select "Full Stack"
- [ ] Verify both services start
- [ ] Open http://localhost:5000 in browser
- [ ] Test API with `api_tests.http`

---

## 🔧 Common Operations

### Install Dependencies
```
Ctrl+Shift+P → Tasks: Run Task → Install All Dependencies
```

### Start Services
```
F5 → Select "Full Stack (Frontend + Backend)"
```

### Test Backend API
```
Ctrl+Shift+P → Tasks: Run Task → Run Backend Tests
```

### View Logs
```
Ctrl+Shift+P → Tasks: Run Task → View All Logs
```

### Stop Everything
```
Shift+F5 (if running via debug)
OR
Ctrl+Shift+P → Tasks: Run Task → Stop All Services
```

---

## 🎯 Debugging Tips

1. **Set Breakpoints:** Click left margin (red dot appears)
2. **Start Debug:** Press `F5`
3. **Step Through:**
   - `F10` - Step Over
   - `F11` - Step Into
   - `Shift+F11` - Step Out
4. **Inspect:** Hover over variables to see values
5. **Continue:** Press `F5` to continue execution

---

## 🔍 Viewing Logs

### Method 1: Tasks (Real-time)
```
Ctrl+Shift+P → Tasks: Run Task → View All Logs
```

### Method 2: Open Files
- `logs/backend_service.log`
- `logs/frontend_service.log`

### Method 3: Terminal
```powershell
Get-Content logs\backend_service.log -Wait -Tail 20
```

---

## 🛑 Stopping Services

### If running via Debug (F5):
Press `Shift+F5`

### If running via Tasks:
```
Ctrl+Shift+P → Tasks: Run Task → Stop All Services
```

### Manual:
```powershell
# Kill all Python processes in project
Get-Process python | Where-Object {$_.Path -like '*project*'} | Stop-Process -Force
```

---

## 📦 Recommended Extensions

When you open the project, VS Code will suggest installing:

**Essential:**
- Python
- Pylance
- Python Debugger

**Helpful:**
- REST Client (for `api_tests.http`)
- SQLite (view databases)
- GitLens
- PowerShell

Click **"Install All"** when prompted.

---

## 💡 Pro Tips

### 1. Split Terminal
Press `Ctrl+Shift+5` to split terminal and view multiple logs simultaneously.

### 2. Multiple Debug Sessions
The "Full Stack" configuration launches both services in separate debug sessions.

### 3. Task Automation
Create custom tasks in `.vscode/tasks.json` for repetitive operations.

### 4. API Testing
Use `api_tests.http` for quick API testing without leaving VS Code.

### 5. Log Monitoring
Use "View All Logs" task to monitor both services in real-time.

---

## 🆘 Troubleshooting

### Debug Config Not Found
1. Install Python extension
2. Reload window: `Ctrl+Shift+P` → "Reload Window"
3. Select Python interpreter

### Port Already in Use
Run task: "Stop All Services" then try again

### Tasks Not Working
Check terminal is PowerShell (default in settings.json)

### Extensions Not Installing
Open Extensions panel (`Ctrl+Shift+X`) and install manually

---

## 📖 Full Documentation

For complete details, see [`.vscode/README.md`](.vscode/README.md)

---

**Created:** November 12, 2025  
**For:** Integrated Geometry Learning System  
**Quick access:** Keep this file open as reference!
