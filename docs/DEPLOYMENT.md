# BuildPilot AI — Production Deployment Guide

This guide provides end-to-end instructions for deploying **BuildPilot AI** into production using:
- **Frontend**: React + Vite + TypeScript hosted on **Vercel**
- **Backend**: Python 3.11+ + FastAPI hosted on **Render** (Free / Starter Web Service)
- **Database**: **MongoDB Atlas** (Cloud M0 Free Tier / Production Cluster) + SQLite for relational metadata
- **AI Integration**: **Google Gemini API** (`gemini-3.8-flash`)
- **Version Control**: **GitHub**

---

## Architecture Overview

```
                      ┌──────────────────────────────────────────┐
                      │              User Browser                │
                      └────────────────────┬─────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    │                                             │
                    ▼ HTTPS                                       ▼ HTTPS
     ┌─────────────────────────────┐               ┌─────────────────────────────┐
     │      Vercel Hosting         │               │        Render Cloud         │
     │  (React + Vite Single Page) │               │   (FastAPI Backend Service) │
     │  https://your-app.vercel.app│               │https://your-api.onrender.com│
     └──────────────┬──────────────┘               └──────────────┬──────────────┘
                    │                                             │
                    │ VITE_API_BASE_URL (REST / WebSockets)       │
                    └─────────────────────────────────────────────┤
                                                                  │
                                           ┌──────────────────────┴──────────────────────┐
                                           │                                             │
                                           ▼ TLS 1.3                                     ▼ HTTPS
                            ┌─────────────────────────────┐               ┌─────────────────────────────┐
                            │     MongoDB Atlas (M0+)     │               │      Google Gemini API      │
                            │ (Projects & Multi-Agent DB) │               │  (gemini-3.8-flash Models)  │
                            └─────────────────────────────┘               └─────────────────────────────┘
```

---

## Phase 1: GitHub Repository Setup

1. **Initialize Git (if not already done)** in the project root:
   ```bash
   git init
   git add .
   git commit -m "feat: complete buildpilot ai production preparation"
   ```

2. **Create a new GitHub Repository**:
   - Go to [GitHub New Repository](https://github.com/new).
   - Set the repository name (e.g., `buildpilot-ai`).
   - Keep it **Private** or **Public** depending on your preference.

3. **Push local code to GitHub**:
   ```bash
   git remote add origin https://github.com/<your-username>/buildpilot-ai.git
   git branch -M main
   git push -u origin main
   ```

> [!IMPORTANT]
> Verify that `.env` files are ignored by git (`git status` must never show `.env`). All secrets must be configured via cloud dashboard environment variables.

---

## Phase 2: MongoDB Atlas Setup

1. **Create an Atlas Account & Cluster**:
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a free **M0 Shared Cluster** (e.g., AWS / Oregon region for low latency with Render Oregon).
   - Name your database cluster (e.g., `Cluster0`).

2. **Configure Database User & Credentials**:
   - Navigate to **Security** -> **Database Access**.
   - Click **Add New Database User**.
   - Authentication Method: **Password**.
   - Username: `buildpilot_user`
   - Password: `<Generate-Strong-Password>` (copy this securely).
   - Database User Privileges: **Read and write to any database** (or `Built-in role: Atlas Admin` / `readWriteAnyDatabase`).

3. **Configure Network Access**:
   - Navigate to **Security** -> **Network Access**.
   - Click **Add IP Address**.
   - Select **Allow Access from Anywhere** (`0.0.0.0/0`) since Render dynamic egress IPs change frequently.
   - Confirm and wait for the status to become **Active**.

4. **Obtain Connection String**:
   - Go to **Database** -> **Clusters** -> Click **Connect**.
   - Choose **Drivers** (Python 3.12+).
   - Copy the SRV connection string:
     ```text
     mongodb+srv://buildpilot_user:<password>@cluster0.mongodb.net/buildpilot?retryWrites=true&w=majority
     ```
   - Replace `<password>` with your actual database user password.

---

## Phase 3: Render Backend Deployment

1. **Log in to Render**:
   - Open [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** -> **Web Service**.

2. **Connect GitHub Repository**:
   - Connect your GitHub account and select your `buildpilot-ai` repository.

3. **Configure Web Service Settings**:
   - **Name**: `buildpilot-backend` (or your chosen name)
   - **Region**: `Oregon (US West)` (matches Atlas default)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     python run.py
     ```
   - **Instance Type**: `Free` (or `Starter` for zero cold-starts)

4. **Add Backend Environment Variables** in the Render Dashboard (**Environment** tab):

| Variable Key | Suggested Production Value | Description |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.11.9` | Ensures modern CPython runtime |
| `PORT` | `10000` | Port automatically assigned by Render |
| `HOST` | `0.0.0.0` | Bind to all interfaces for public routing |
| `GEMINI_API_KEY` | `AIzaSy...` | Your Google Gemini API Key from Google AI Studio |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Production high-speed model |
| `MONGODB_URI` | `mongodb+srv://buildpilot_user:<pwd>@cluster0...` | MongoDB Atlas SRV URI |
| `CORS_ORIGINS` | `https://*.vercel.app,https://your-custom-domain.com` | Allowed CORS origins for browser client |
| `MAX_UPLOAD_SIZE_MB`| `10` | Maximum file upload limit in MB |

5. **Configure Health Check**:
   - Under **Advanced Settings** -> **Health Check Path**: enter `/health`.
   - Click **Create Web Service**.
   - Wait 2–3 minutes for build and deployment.
   - Once complete, copy the service URL (e.g., `https://buildpilot-backend.onrender.com`).

---

## Phase 4: Vercel Frontend Deployment

1. **Log in to Vercel**:
   - Open [Vercel Dashboard](https://vercel.com/dashboard).
   - Click **Add New...** -> **Project**.

2. **Import GitHub Repository**:
   - Select your `buildpilot-ai` repository.

3. **Configure Project Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Add Frontend Environment Variables**:

| Variable Key | Production Value |
| :--- | :--- |
| `VITE_API_BASE_URL` | `https://buildpilot-backend.onrender.com/api` |

*(Make sure to use your actual Render backend URL followed by `/api`)*.

5. **Deploy**:
   - Click **Deploy**.
   - Vercel automatically bundles the Vite application with code splitting, runs post-processing, and maps SPA rewrites via `frontend/vercel.json`.
   - Once deployed, you receive your public production URL (e.g., `https://buildpilot-ai.vercel.app`).

---

## Phase 5: Verification & End-to-End Testing

Once both services are deployed, test the following checklist:

| Verification Item | Action | Expected Result |
| :--- | :--- | :--- |
| **Backend Health** | Open `https://<backend>.onrender.com/health` in browser | `{"status":"healthy","service":"BuildPilot AI Backend",...}` |
| **API Health** | Open `https://<backend>.onrender.com/api/health` | HTTP 200 with diagnostics, `mongodb_connected: true` |
| **Swagger Docs** | Open `https://<backend>.onrender.com/docs` | Interactive OpenAPI documentation loads |
| **Frontend Load** | Open `https://<frontend>.vercel.app` | BuildPilot AI interface loads instantly with theme support |
| **CORS Verification** | Inspect Network tab in DevTools | No CORS errors; `Access-Control-Allow-Origin` returns client origin |
| **Project Creation** | Click **New Project** and submit prompt | Multi-Agent Orchestrator executes all 6 agents (Planner to QA) |
| **Live Preview** | Inspect iframe in studio | Generated responsive web app renders interactively across viewports |
| **ZIP Download** | Click **Export ZIP** | Complete source workspace downloads as `.zip` archive |
| **Assistant Tools** | Ask math: *"15 * 84 + 19"*; ask search: *"Latest Python"* | Assistant responds with AST calculator and DuckDuckGo citations |

---

## Phase 6: Custom Domain Setup (Optional)

### Adding Custom Domain to Vercel
1. In Vercel Project Dashboard: **Settings** -> **Domains**.
2. Enter your domain (e.g. `app.yourdomain.com`).
3. Add the `CNAME` record in your DNS provider:
   - Host: `app`
   - Type: `CNAME`
   - Value: `cname.vercel-dns.com`

### Adding Custom Domain to Render
1. In Render Web Service Dashboard: **Settings** -> **Custom Domains**.
2. Enter `api.yourdomain.com`.
3. Add the `CNAME` record in your DNS provider:
   - Host: `api`
   - Type: `CNAME`
   - Value: `buildpilot-backend.onrender.com`
4. Update `VITE_API_BASE_URL` in Vercel to `https://api.yourdomain.com/api` and redeploy.

---

## Troubleshooting Guide

### 1. Render Free Tier Cold Starts
- **Symptom**: First request takes 30-50 seconds to respond.
- **Cause**: Render Free tier spins down inactive instances after 15 minutes of inactivity.
- **Solution**: The frontend displays a smooth loading indicator. For zero latency, upgrade to Render Starter plan ($7/mo) or use a free uptime monitor (e.g. UptimeRobot or Cron-job.org) pinging `https://<backend>.onrender.com/health` every 10 minutes.

### 2. MongoDB DNS Resolution Error (`ServerSelectionTimeoutError`)
- **Symptom**: `ServerSelectionTimeoutError: No replica set members found`.
- **Cause**: IP not whitelisted in Atlas or missing `dnspython`.
- **Fix**:
  1. In Atlas, verify **Network Access** includes `0.0.0.0/0` (Allow from anywhere).
  2. Verify database username and password are correct.
  3. Notice `dnspython>=2.6.1` and `pymongo>=4.8.0` are already pinned in `requirements.txt`.

### 3. CORS Missing Header Error
- **Symptom**: Browser console logs `Access to XMLHttpRequest at '...' from origin '...' has been blocked by CORS policy`.
- **Fix**:
  1. In Render Environment variables, add your Vercel origin to `CORS_ORIGINS`:
     ```text
     CORS_ORIGINS=https://buildpilot-ai.vercel.app,https://*.vercel.app
     ```
  2. Backend automatically includes regex matching for `r"https://.*\.vercel\.app"`.

### 4. SPA Page Refresh Returns 404
- **Symptom**: Navigating directly to a URL route returns 404 on Vercel.
- **Fix**: The included `frontend/vercel.json` already contains the SPA rewrite:
  ```json
  {
    "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
  }
  ```

---

## Rollback Plan

If a faulty deployment occurs:

1. **Vercel Rollback**:
   - Go to Vercel Project -> **Deployments**.
   - Locate the previous stable build.
   - Click the three dots `...` -> **Promote to Production** (instant zero-downtime rollback).

2. **Render Rollback**:
   - Go to Render Dashboard -> **Deploys**.
   - Select the last successful commit deploy -> Click **Rollback**.
