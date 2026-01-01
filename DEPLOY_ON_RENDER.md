# How to Deploy on Render (Recommended for Bulk Emails)

Render is excellent for this app because it provides a proper **Web Service** that doesn't timeout quickly like Vercel, making it perfect for sending bulk emails.

---

## 🚀 Deployment Steps

1.  **Sign Up / Login**
    *   Go to **[render.com](https://render.com)** and create a free account.

2.  **Create New Service**
    *   Click **"New +"** button.
    *   Select **"Web Service"**.

3.  **Connect GitHub**
    *   Connect your GitHub account.
    *   Search for your repo: `Ai-Agent-For-Mail-Automation` and click **Connect**.

4.  **Configure Settings**
    *   **Name**: `mail-agent` (or anything you like).
    *   **Region**: Closest to you (e.g., Singapore/Frankfurt).
    *   **Branch**: `main`.
    *   **Runtime**: `Python 3`.
    *   **Build Command**: `pip install -r requirements.txt` (Default is fine).
    *   **Start Command**: `gunicorn app:app`
        *   *(Important: This tells Render to run your app using Gunicorn server).*

5.  **Enter Environment Variables (The Secret Keys)**
    *   Scroll down to **"Advanced"** or **"Environment Variables"**.
    *   Click **"Add Environment Variable"** and add these (from your `.env` file):

    | Key | Value |
    | :--- | :--- |
    | `SMTP_SERVER` | `smtp.gmail.com` |
    | `SMTP_PORT` | `465` |
    | `SMTP_USER` | `fmax41309@gmail.com` (Your Email) |
    | `SMTP_PASSWORD` | `utvl wspp mwtr eqcf` (Your App Password) |
    | `SMTP_USE_SSL` | `true` |

6.  **Deploy!**
    *   Click **"Create Web Service"**.
    *   Wait for 1-2 minutes. Render will install everything and start the app.
    *   Once you see "Live", click the URL (e.g., `https://mail-agent.onrender.com`).

---

## ✅ Why Render?
*   **No Timeouts**: Unlike Vercel (10s limit), Render keeps running, so you can send 1000+ emails without the process taking getting killed.
*   **Free Tier**: Their free tier is generous enough for personal tools.
