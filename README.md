# 🚀 BuildPilot AI — Autonomous Multi-Agent Software Engineering Platform

A full-stack, production-grade **Autonomous Multi-Agent Software Engineering Platform & AI Assistant** built with **FastAPI**, **React 18**, **TypeScript**, **Vite 5**, **Tailwind CSS v3**, **MongoDB**, and **Google Gemini API** (`gemini-3.8-flash`).

BuildPilot AI orchestrates six specialist AI agents to autonomously plan, design, architect, generate, verify, and preview complete, working web applications with real functional capabilities and zero placeholder buttons.

---

## 🌟 Core Platform Capabilities

### 1. 🤖 7-Agent Autonomous Software Engineering Mesh
1. **Planner Agent**: Deconstructs requirements into software architectures, component trees, API specs, and task dependency graphs.
2. **UI/UX Agent**: Generates color systems, responsive breakpoints (360px, 390px, 768px, 1024px, 1440px), wireframes, and design tokens.
3. **Database Agent**: Formulates document models, compound index strategies, and seed datasets for MongoDB.
4. **Backend Agent**: Formulates production FastAPI REST endpoints, Pydantic validation schemas, and business logic.
5. **Frontend Agent**: Generates interactive React/Tailwind components, state hooks, and event handlers.
6. **QA Agent**: Audits generated code, ensures zero placeholder buttons, and runs verification assertions.
7. **Agent Orchestrator**: Coordinates execution sequence, tracks progress, streams telemetry, and generates sandboxed workspaces.

### 2. ⚡ Real Working Generated Projects (Zero Fake Buttons)
- **🏨 Luxury Hotel Booking Website**: Live room inventory catalog, interactive check-in/out date picker, duration calculator, amenity filters, booking modal with tax calculations, and instant confirmation toast.
- **🛍️ E-Commerce with Admin Dashboard**: Product grid, instant search filter, slide-over shopping cart drawer with quantity adjustments, checkout dialog, and toggleable Admin Analytics Dashboard with revenue metrics and stock restocker.
- **💼 Developer Portfolio with Contact Form**: Modern dark aesthetic, domain-based project filtering, and interactive validated contact form.
- **📋 Task Management Kanban Board**: 3-column Kanban workflow (To Do, In Progress, Done) with status progression, new task creator dialog, priority pills, and task deletion.

### 3. 🖥️ Interactive Split-Screen Live Preview & Viewport Testing
- Real-time interactive iframe preview of generated web applications.
- Instant responsive viewport switching:
  - 📱 **360px** (Small Mobile)
  - 📱 **390px** (Standard Mobile)
  - 📱 **768px** (Tablet)
  - 💻 **1024px** (Laptop)
  - 🖥️ **1440px** (Full Desktop)
- Export generated projects directly as `.zip` archives.
- Sandboxed file tree viewer and code inspector.

### 4. 💬 Integrated AI Assistant & Tool Execution
- Multi-turn conversation assistant with SQLite persistence and memory context.
- **🧮 AST-Based Safe Calculator**: Computes arithmetic, trigonometry, roots, and logarithms without code injection risks.
- **🌐 Live Web Search**: Real-time web lookups via DuckDuckGo (`ddgs`) with zero paid search keys needed.
- **📄 Document Reader**: Upload and analyze PDF and TXT documents.
- **🛡️ Consequential Action Gate**: Enforces user confirmation before executing sensitive actions.

---

## 🏗️ Architecture & Project Structure

```
BuildPilot AI/
├── backend/
│   ├── app/
│   │   ├── agents/                  # 7 Specialist Agents & Orchestrator
│   │   │   ├── base_agent.py        # Base agent with retry & timing logic
│   │   │   ├── planner_agent.py     # Architecture planner
│   │   │   ├── uiux_agent.py        # Design system & responsive layout agent
│   │   │   ├── database_agent.py    # MongoDB schemas & indexes agent
│   │   │   ├── backend_agent.py     # FastAPI endpoints agent
│   │   │   ├── frontend_agent.py    # Interactive React components agent
│   │   │   ├── qa_agent.py          # Quality assurance & verification agent
│   │   │   └── orchestrator.py      # Master pipeline orchestrator
│   │   ├── api/                     # REST API Routers
│   │   │   ├── projects.py          # Project generation, preview & ZIP export
│   │   │   ├── chat.py              # Assistant message turns & action confirmation
│   │   │   ├── conversations.py     # Conversation sessions CRUD
│   │   │   ├── documents.py         # PDF & TXT document upload and parsing
│   │   │   └── health.py            # System health & diagnostics
│   │   ├── core/                    # Configuration & database connections
│   │   │   ├── config.py            # Pydantic v2 SettingsConfigDict
│   │   │   ├── database.py          # SQLite engine & sessionmaker
│   │   │   └── mongodb.py           # MongoDB store with resilient fallback
│   │   ├── generators/              # Workspace sandbox & project presets
│   │   │   ├── presets.py           # Hotel, E-commerce, Portfolio, Task presets
│   │   │   └── workspace_manager.py # Sandboxed file writing & ZIP builder
│   │   ├── models/                  # Database models
│   │   │   └── db_models.py         # SQLAlchemy models (UTC timezone-aware)
│   │   ├── schemas/                 # Pydantic validation schemas
│   │   │   └── api_schemas.py       # ConfigDict request/response schemas
│   │   ├── services/                # Application services
│   │   │   ├── agent_service.py     # Assistant execution orchestrator
│   │   │   ├── gemini_service.py    # Google GenAI SDK interface
│   │   │   └── memory_service.py    # Context history manager
│   │   ├── tools/                   # Assistant tools
│   │   │   ├── calculator.py        # AST safe math parser
│   │   │   ├── web_search.py        # DuckDuckGo search integration
│   │   │   ├── doc_reader.py        # PDF & TXT text extraction
│   │   │   └── action_tool.py       # Consequential action confirmation tool
│   │   ├── generated_projects/      # Isolated sandboxed project directories
│   │   ├── uploads/                 # Uploaded document files
│   │   └── main.py                  # FastAPI root & static React app mount
│   ├── tests/
│   │   └── test_buildpilot.py       # Pytest automated test suite (12 test cases)
│   ├── requirements.txt             # Python dependencies
│   ├── run.py                       # Single-command backend runner
│   ├── .env.example                 # Environment template
│   └── .env                         # Local configuration
├── frontend/
│   ├── dist/                        # Production React build (auto-served by backend)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProjectCreatorModal.jsx # New project prompt & presets modal
│   │   │   ├── AgentWorkflowViewer.jsx # Multi-agent timeline & specs inspector
│   │   │   ├── LivePreviewPanel.jsx    # Responsive split-screen preview (360px - 1440px)
│   │   │   ├── FileTreeViewer.jsx      # Workspace file tree & code viewer
│   │   │   ├── Sidebar.jsx             # Collapsible conversation drawer
│   │   │   ├── ChatArea.jsx            # Assistant chat feed & starter cards
│   │   │   ├── ChatInput.jsx           # Auto-expanding input with file upload
│   │   │   ├── FileUploadModal.jsx     # Drag-and-drop document upload dialog
│   │   │   ├── ActionConfirmModal.jsx  # Security checkpoint dialog
│   │   │   └── ToolExecutionBadge.jsx  # Expandable tool call cards
│   │   ├── hooks/
│   │   │   └── useTheme.js             # Dark / Light theme toggle
│   │   ├── services/
│   │   │   └── api.js                  # Axios client
│   │   ├── App.jsx                     # Root application coordinator (Studio + Chat)
│   │   ├── index.css                   # Tailwind styles
│   │   └── main.jsx                    # React entrypoint
│   ├── index.html                   # HTML shell with Google Fonts
│   ├── package.json                 # Frontend dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   ├── tailwind.config.js           # Tailwind theme configuration
│   └── vite.config.js               # Vite build configuration
├── docs/
│   ├── TESTING_AUDIT.md             # Complete project audit & gaps analysis
│   ├── FINAL_TEST_REPORT.md         # Final test report (100% pass rate)
│   ├── BUG_FIX_REPORT.md            # Auto bug fixing & root cause report
│   ├── PERFORMANCE_REPORT.md        # Latency, bundle sizes, and token metrics
│   └── SECURITY_REPORT.md           # Threat modeling & security gates report
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-container orchestration (App + Mongo)
├── start_app.bat                    # Windows 1-click launcher
├── start_app.ps1                    # PowerShell launcher
├── .gitignore                       # Git ignore rules
└── README.md                        # Documentation
```

---

## 🛠️ Windows Setup Guide

### 1. Prerequisites
- **Python 3.10+** (verified on Python 3.12 and 3.15)
- **Node.js 18+** & **npm**

---

### 2. Environment Configuration
Edit `backend/.env` (or copy from `.env.example`):
```env
# Google AI Studio API Key (Optional — autonomous tool mode runs if empty)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash

PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
DATABASE_URL=sqlite:///./ai_assistant.db
MONGODB_URL=mongodb://localhost:27017/buildpilot
MAX_UPLOAD_SIZE_MB=10
```

---

### 3. Launching the Application

#### Option A: One-Click Launch (Recommended)
Double-click `start_app.bat` or run:
```powershell
.\start_app.bat
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

#### Option B: Docker Compose
```bash
docker compose up --build
```
Access the application at `http://localhost:8000`.

---

## 🧪 Automated Testing Suite

Run the complete Pytest automated test suite:
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/test_buildpilot.py -v
```

### Verified Test Results:
```
tests/test_buildpilot.py::test_planner_agent PASSED                      [  8%]
tests/test_buildpilot.py::test_uiux_agent PASSED                         [ 16%]
tests/test_buildpilot.py::test_database_agent PASSED                     [ 25%]
tests/test_buildpilot.py::test_backend_agent PASSED                      [ 33%]
tests/test_buildpilot.py::test_frontend_agent PASSED                     [ 41%]
tests/test_buildpilot.py::test_qa_agent PASSED                           [ 50%]
tests/test_buildpilot.py::test_orchestrator_pipeline_hotel PASSED        [ 58%]
tests/test_buildpilot.py::test_orchestrator_pipeline_ecommerce PASSED    [ 66%]
tests/test_buildpilot.py::test_orchestrator_pipeline_portfolio PASSED    [ 75%]
tests/test_buildpilot.py::test_orchestrator_pipeline_task_manager PASSED [ 83%]
tests/test_buildpilot.py::test_api_health PASSED                         [ 91%]
tests/test_buildpilot.py::test_api_project_lifecycle PASSED              [100%]
======================== 12 passed, 1 warning in 8.79s ========================
```

---

## 📡 REST API Reference

| Endpoint | Method | Purpose |
|---|---|---|
| `GET /api/health` | `GET` | Health status, active specialist agents, model information |
| `POST /api/projects` | `POST` | Trigger multi-agent pipeline and generate application |
| `GET /api/projects` | `GET` | List all generated projects |
| `GET /api/projects/{id}` | `GET` | Detailed project telemetry and file tree |
| `GET /api/projects/{id}/preview` | `GET` | Serve live interactive HTML application in iframe |
| `GET /api/projects/{id}/files/{path}` | `GET` | Read individual project file with path traversal protection |
| `GET /api/projects/{id}/export` | `GET` | Download generated project as `.zip` archive |
| `DELETE /api/projects/{id}` | `DELETE` | Cascade remove project from database and filesystem |
| `POST /api/conversations/{id}/messages` | `POST` | Chat turn with tool calling (Calculator, Search, Docs) |
| `POST /api/documents/upload` | `POST` | Upload and sanitize PDF/TXT documents (max 10MB) |
| `GET /docs` | `GET` | Interactive Swagger API documentation |

---

## 🚀 Cloud Production Deployment

BuildPilot AI is fully configured for zero-friction cloud deployment:
- **Frontend Hosting**: [Vercel](https://vercel.com/) (configured via `frontend/vercel.json`)
- **Backend Hosting**: [Render](https://render.com/) (configured via `render.yaml`)
- **Database**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (M0 Free Tier or Dedicated Cluster)

For complete, step-by-step instructions on setting up GitHub, Atlas, Render, Vercel, custom domains, and environment variables, see [**`docs/DEPLOYMENT.md`**](file:///docs/DEPLOYMENT.md).

For a detailed breakdown of the 7-agent mesh, ReAct engine, security defenses, and complete directory catalog, see [**`docs/ARCHITECTURE.md`**](file:///docs/ARCHITECTURE.md).
