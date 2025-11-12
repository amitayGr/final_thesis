# VS Code Configuration Guide

This directory contains VS Code configuration files for the Integrated Geometry Learning System project.

---

## 📁 Configuration Files

### 1. `launch.json` - Debug Configurations

Defines debug configurations for running and debugging the application.

**Available Debug Configurations:**

#### Individual Services:
- **Backend Service** - Debug backend API on port 5001
- **Frontend Service** - Debug frontend on port 5000
- **Backend API Tests** - Debug the test_api.py script

#### Compound Configuration:
- **Full Stack (Frontend + Backend)** - Launch both services simultaneously

**How to Use:**
1. Open Debug panel (Ctrl+Shift+D)
2. Select configuration from dropdown
3. Press F5 or click green play button

**Features:**
- ✅ Separate terminals for each service
- ✅ Environment variables pre-configured
- ✅ Debug mode enabled
- ✅ Breakpoint support

---

### 2. `tasks.json` - Build & Run Tasks

Defines tasks for common development operations.

**Available Tasks:**

#### Installation:
- **Install Backend Dependencies** - `pip install -r requirements.txt` for backend
- **Install Frontend Dependencies** - `pip install -r requirements.txt` for frontend
- **Install All Dependencies** - Install both in sequence

#### Running Services:
- **Start Backend Service** - Start backend on port 5001
- **Start Frontend Service** - Start frontend on port 5000
- **Start Both Services** - Start both simultaneously

#### Testing:
- **Run Backend Tests** - Execute test_api.py
- **Validate Project Structure** - Run validate_project.py

#### Logging:
- **View Backend Logs** - Real-time backend log viewing
- **View Frontend Logs** - Real-time frontend log viewing
- **View All Logs** - Both logs in separate panels
- **Clean Logs** - Delete all log files

#### Utilities:
- **Open Browser (Frontend)** - Open http://localhost:5000
- **Open Browser (Backend API)** - Open http://localhost:5001/api/health
- **Stop All Services** - Kill all running Python services
- **Check Python** - Verify Python installation

**How to Use:**
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select desired task

**Quick Commands:**
- `Ctrl+Shift+B` - Run default build task
- Terminal → Run Task...

---

### 3. `settings.json` - Workspace Settings

Project-specific VS Code settings.

**Configured Settings:**

#### Python:
- Default interpreter: system Python
- Linting: Flake8 enabled
- Formatting: Black (optional)
- Auto-environment activation

#### Files:
- Hide `__pycache__`, `.pyc`, `flask_session`
- Auto-save after 1 second
- UTF-8 encoding
- LF line endings
- Trim trailing whitespace

#### Editor:
- Tab size: 4 spaces (Python), 2 spaces (JSON)
- Rulers at 80 and 120 characters
- Insert spaces instead of tabs

#### Terminal:
- Default: PowerShell
- Working directory: workspace root

---

### 4. `extensions.json` - Recommended Extensions

List of recommended VS Code extensions for this project.

**Recommended Extensions:**

#### Essential:
- **Python** (ms-python.python) - Python language support
- **Pylance** (ms-python.vscode-pylance) - Fast Python language server
- **Python Debugger** (ms-python.debugpy) - Debugging support

#### Web Development:
- **Jinja** (wholroyd.jinja) - Jinja template syntax

#### Database:
- **SQLite** (alexcvzz.vscode-sqlite) - View and edit SQLite databases

#### API Testing:
- **REST Client** (humao.rest-client) - Test API endpoints in VS Code

#### Productivity:
- **GitLens** (eamodio.gitlens) - Enhanced Git support
- **Markdown All in One** (yzhang.markdown-all-in-one) - Markdown tools
- **PowerShell** (ms-vscode.powershell) - PowerShell support
- **Better Comments** (aaron-bond.better-comments) - Colorful comments

**How to Install:**
1. Open Extensions panel (Ctrl+Shift+X)
2. VS Code will prompt to install recommended extensions
3. Click "Install All"

---

### 5. `api_tests.http` - REST API Testing

HTTP request file for testing backend API directly in VS Code.

**Requires:** REST Client extension

**How to Use:**
1. Open `api_tests.http`
2. Click "Send Request" above any request
3. Or use `Ctrl+Alt+R` to send request

**Available Tests:**
- Health check
- Complete session workflow
- Individual endpoint tests
- Error testing scenarios

**Features:**
- ✅ Pre-configured requests
- ✅ Variables for URLs
- ✅ Complete workflow examples
- ✅ Error test cases

---

## 🚀 Quick Start Guide

### First Time Setup

1. **Open Project in VS Code:**
   ```bash
   cd c:\Users\lahavor\am\final_thesis\project
   code .
   ```

2. **Install Recommended Extensions:**
   - VS Code will prompt you
   - Click "Install All"

3. **Install Dependencies:**
   - Press `Ctrl+Shift+P`
   - Run task: "Install All Dependencies"

### Running the Application

#### Method 1: Debug Panel (Recommended)
1. Press `Ctrl+Shift+D` (open Debug panel)
2. Select "Full Stack (Frontend + Backend)"
3. Press `F5`

Both services will start in separate terminals with debugging enabled.

#### Method 2: Tasks
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Start Both Services"

#### Method 3: Manual
1. Open terminal (`Ctrl+`` `)
2. Run commands:
   ```powershell
   # Terminal 1
   cd backend_service
   python app.py
   
   # Terminal 2 (split terminal)
   cd frontend_service
   python app.py
   ```

---

## 🔧 Common Workflows

### Development Workflow

1. **Start Services:**
   - F5 → Select "Full Stack"

2. **Make Changes:**
   - Edit code
   - Save (auto-save enabled)

3. **Test:**
   - Open `api_tests.http`
   - Send requests
   - Or run "Backend API Tests"

4. **View Logs:**
   - Run task: "View All Logs"
   - Check `logs/` directory

5. **Stop Services:**
   - Run task: "Stop All Services"
   - Or close debug session

### Testing Workflow

1. **Start Backend:**
   - F5 → "Backend Service"

2. **Run Tests:**
   - Open `backend_service/test_api.py`
   - F5 → "Backend API Tests"
   - Or run task: "Run Backend Tests"

3. **Manual API Testing:**
   - Open `api_tests.http`
   - Send individual requests

### Debugging Workflow

1. **Set Breakpoints:**
   - Click left margin in code

2. **Start Debug:**
   - F5 → Select appropriate config

3. **Debug Controls:**
   - F10 - Step Over
   - F11 - Step Into
   - Shift+F11 - Step Out
   - F5 - Continue

4. **Inspect Variables:**
   - Hover over variables
   - Check Debug panel

---

## 📊 Task Reference

### Quick Task Commands

```
Ctrl+Shift+P → Tasks: Run Task → [Select Task]
```

**Most Used Tasks:**
1. Start Both Services
2. Run Backend Tests
3. View All Logs
4. Install All Dependencies
5. Stop All Services

---

## 🎯 Keyboard Shortcuts

### Debugging:
- `F5` - Start/Continue debugging
- `Shift+F5` - Stop debugging
- `Ctrl+Shift+F5` - Restart debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out

### Tasks:
- `Ctrl+Shift+B` - Run build task
- `Ctrl+Shift+P` - Command palette (run tasks)

### Terminal:
- `Ctrl+`` - Toggle terminal
- `Ctrl+Shift+`` - New terminal
- `Ctrl+Shift+5` - Split terminal

### General:
- `Ctrl+Shift+D` - Debug panel
- `Ctrl+Shift+E` - Explorer
- `Ctrl+Shift+F` - Search
- `Ctrl+Shift+X` - Extensions

---

## 🔍 Troubleshooting

### Python Extension Issues

**Problem:** Debug configurations not working

**Solution:**
1. Install Python extension (ms-python.python)
2. Reload VS Code (Ctrl+Shift+P → "Reload Window")
3. Select Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")

### Task Execution Issues

**Problem:** Tasks fail to run

**Solution:**
1. Check Python is installed: Run task "Check Python"
2. Verify working directory in tasks.json
3. Check PowerShell is default terminal

### Port Already in Use

**Problem:** Service won't start (port conflict)

**Solution:**
1. Run task: "Stop All Services"
2. Or manually:
   ```powershell
   netstat -ano | findstr :5001
   taskkill /PID <PID> /F
   ```

### Logs Not Visible

**Problem:** Log viewing tasks show empty

**Solution:**
1. Start services first
2. Run task: "View All Logs"
3. Or manually open files in `logs/` directory

---

## 📝 Customization

### Adding Custom Tasks

Edit `.vscode/tasks.json`:

```json
{
    "label": "My Custom Task",
    "type": "shell",
    "command": "python my_script.py",
    "options": {
        "cwd": "${workspaceFolder}"
    },
    "problemMatcher": []
}
```

### Adding Debug Configurations

Edit `.vscode/launch.json`:

```json
{
    "name": "My Debug Config",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/my_script.py",
    "console": "integratedTerminal"
}
```

### Changing Settings

Edit `.vscode/settings.json` to customize:
- Editor behavior
- Python linting rules
- File associations
- Terminal preferences

---

## 📚 Additional Resources

- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks)
- [Python in VS Code](https://code.visualstudio.com/docs/languages/python)
- [REST Client Extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

---

## ✅ Checklist: Is Everything Working?

- [ ] Python extension installed
- [ ] Can open Debug panel (Ctrl+Shift+D)
- [ ] See debug configurations in dropdown
- [ ] Can run tasks (Ctrl+Shift+P → Tasks)
- [ ] Dependencies installed (both services)
- [ ] Can start services via F5
- [ ] Both services run without errors
- [ ] Can view logs
- [ ] Can test API with api_tests.http
- [ ] Breakpoints work when debugging

If all checked ✅, you're ready to develop!

---

**Created:** November 12, 2025  
**For Project:** Integrated Geometry Learning System  
**VS Code Version:** 1.80+
