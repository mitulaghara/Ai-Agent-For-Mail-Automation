# How to Deploy on Vercel

Since this app uses Flask and SMTP, it can be deployed on Vercel using their Python runtime.

## ⚠️ Important Limitation
Vercel is "Serverless". This means:
*   Processes shouldn't run for more than **10-60 seconds**.
*   Sending **Bulk Emails (100+)** might timeout.
*   **Recommendation:** For small lists (10-50 emails), Vercel is fine. For larger lists, run this locally or on a standard server like Render.

---

## 🚀 Steps to Deploy

### 1. Install CLI
If you haven't installed Vercel CLI:
```bash
npm i -g vercel
```

### 2. Login
```bash
vercel login
```

### 3. Deploy
Run the command in your project folder:
```bash
vercel
```
*   Set up and deploy? **Yes**
*   Scope? **(Your username)**
*   Link to existing project? **No**
*   Project Name? **(Press Enter)**
*   Directory? **(Press Enter)**

### 4. Add Environment Variables (Crucial!)
Your app won't work without credentials.
1.  Go to your **Vercel Dashboard** > Select Project > **Settings** > **Environment Variables**.
2.  Add the same keys from your `.env` file:
    *   `SMTP_SERVER`: `smtp.gmail.com`
    *   `SMTP_PORT`: `465`
    *   `SMTP_USER`: `your-email@gmail.com`
    *   `SMTP_PASSWORD`: `your-app-password`
    *   `SMTP_USE_SSL`: `true`

### 5. Redeploy
Once variables are added, you must redeploy for them to take effect:
```bash
vercel --prod
```

Your app is now live! 🌐
