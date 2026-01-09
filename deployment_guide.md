# Online Deployment Guide for DeepKlarity Quiz

This guide explains how to deploy your application to the internet using **Render.com** (recommended for its free tier and ease of use).

**Your GitHub Repository**: [https://github.com/snehalatha-reddy/DeepKlarityQuiz](https://github.com/snehalatha-reddy/DeepKlarityQuiz)

---

## Deployment Strategy
We will deploy two separate services that talk to each other:
1.  **Backend (API)**: Python/FastAPI service.
2.  **Frontend (UI)**: Static React site.

---

## Step 1: Deploy the Backend (API)

1.  **Sign Up/Log In**: Go to [dashboard.render.com](https://dashboard.render.com/).
2.  **New Service**: Click **New +** button and select **Web Service**.
3.  **Connect GitHub**: Select your repository `DeepKlarityQuiz`.
4.  **Configure Settings**:
    - **Name**: `deepklarity-backend`
    - **Root Directory**: `backend` (Important!)
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
      > **CRITICAL**: You MUST include `--host 0.0.0.0` or the deployment will fail!
    - **Free Tier**: Select "Free".
5.  **Environment Variables**:
    Scroll down to "Environment Variables" and add:
    - `Key`: `GROQ_API_KEY`
    - `Value`: `(Paste your actual Groq API Key here)`
    - `Key`: `PYTHON_VERSION`
    - `Value`: `3.10.0`
6.  **Deploy**: Click **Create Web Service**.
    - Wait for the deployment to finish (it might take a few minutes).
    - **Copy the URL** (e.g., `https://deepklarity-backend.onrender.com`). You will need this for the frontend!

---

## Step 2: Deploy the Frontend (UI)

1.  **New Service**: On Render Dashboard, click **New +** and select **Static Site**.
2.  **Connect GitHub**: Select the same repository `DeepKlarityQuiz`.
3.  **Configure Settings**:
    - **Name**: `deepklarity-frontend`
    - **Root Directory**: `frontend` (Important!)
    - **Build Command**: `npm install && npm run build`
    - **Publish Directory**: `dist`
    - **Free Tier**: Select "Free".
4.  **Environment Variables**:
    - `Key`: `VITE_API_URL`
    - `Value`: `(Paste the Backend URL from Step 1)`
    *Example Value: `https://deepklarity-backend.onrender.com`*
5.  **Deploy**: Click **Create Static Site**.
    - Once finished, Render will give you a live URL for your website (e.g., `https://deepklarity-frontend.onrender.com`).

---

## Step 3: Verify

Open your Frontend URL. It should load the "DeepKlarity Quiz" interface. Try generating a quiz to ensure it can talk to the backend.

> **Note**: On the free tier, services might "spin down" after inactivity. The first request might take 30-50 seconds. This is normal for free plans.
