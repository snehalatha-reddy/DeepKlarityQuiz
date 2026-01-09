# Deployment Guide for WikiQuiz

This guide explains how to deploy the application locally using Docker and to the cloud using Render.com.

## Prerequisites
- **Local**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
- **Cloud**: A GitHub account and a [Render](https://render.com) account.

---

## Option 1: Run Locally with Docker (Recommended for Testing)

1.  **Check Environment Variables**:
    Ensure you have a `.env` file in the `backend/` directory with your API keys:
    ```
    GROQ_API_KEY=your_key_here
    ```

2.  **Start the Application**:
    Open a terminal in the project root (`DeepKlarity Asses`) and run:
    ```bash
    docker-compose up --build
    ```

3.  **Access the App**:
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

    *Note: The database (`sql_app.db`) is persisted in the `backend` folder locally.*

---

## Option 2: Deploy to Render.com (Free Tier)

Render is great for this stack because it supports Python backends and Static Frontends easily.

### Step 1: Push Code to GitHub
Ensure your code is pushed to a GitHub repository.

### Step 2: Deploy Backend
1.  Log in to [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repo.
4.  **Settings**:
    - **Name**: `wikiquiz-backend` (or similar)
    - **Root Directory**: `backend`
    - **Environment**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables** (Advanced):
    - Add `GROQ_API_KEY` = `your_actual_key`
    - Add `PYTHON_VERSION` = `3.10.0` (optional, but good for stability)
6.  Click **Create Web Service**.
7.  **Copy the Backend URL** once deployed (e.g., `https://wikiquiz-backend.onrender.com`).

### Step 3: Deploy Frontend
1.  On Render Dashboard, Click **New +** -> **Static Site**.
2.  Connect the same GitHub repo.
3.  **Settings**:
    - **Name**: `wikiquiz-frontend`
    - **Root Directory**: `frontend`
    - **Build Command**: `npm install && npm run build`
    - **Publish Directory**: `dist`
4.  **Environment Variables**:
    - Key: `VITE_API_URL`
    - Value: `https://wikiquiz-backend.onrender.com` (The URL from Step 2)
5.  Click **Create Static Site**.

### Step 4: Finalize
Visit your Frontend URL provided by Render. It should connect to your Backend API.

> **Important Note on Database**:
> This app uses SQLite. On Render's free tier, the filesystem is ephemeral, meaning **your database will reset every time the server restarts or redeploys**.
> For production persistence, you should provision a PostgreSQL database (Render offers a managed one) and update your backend to use `DATABASE_URL` env var.
