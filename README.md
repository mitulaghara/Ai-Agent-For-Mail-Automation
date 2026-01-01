# 📧 AI Mail Automation Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

A powerful, **secure**, and easy-to-use Bulk Email Automation tool with a premium Glassmorphism UI. Send personalized emails to thousands of recipients or single emails instantly using your own Gmail SMTP.

---

## ✨ Features

*   **🎨 Premium Glassmorphism UI**: Modern, dark-themed, and fully responsive design.
*   **📂 Bulk CSV Support**: Drag & drop your contact list to send thousands of emails.
*   **⚡ Single Email Mode**: Quickly send a one-off email without needing a CSV.
*   **🤖 Personalization**: Use `{{name}}` in your message to auto-insert recipient names.
*   **🔒 Secure**: Uses environment variables to keep your credentials safe.
*   **📱 Mobile Ready**: Works perfectly on phones and tablets.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/mitulaghara/Ai-Agent-For-Mail-Automation.git
cd Ai-Agent-For-Mail-Automation
```

### 2. Install Dependencies
Make sure you have Python installed.
```bash
pip install -r requirements.txt
```

### 3. Setup Security (Important!) 🛡️
Create a file named `.env` in the root directory. **NEVER share this file.**

Add your Gmail credentials:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_SSL=true
```
> **Note:** You MUST use a **Google App Password**, not your regular Gmail password.
> Read `HOW_TO_FIX_GMAIL.md` in this repo for a 2-minute setup guide.

### 4. Run the App
```bash
python app.py
```
Visit **http://localhost:5000** (or whatever port is shown) in your browser.

---

## 📝 CSV Format for Bulk Mode
Your CSV file must have these headers:
```csv
email,name
mitul@example.com,Mitul
john@example.com,John Doe
```

---

## ⚠️ Security Notice
*   **Never commit your `.env` file to GitHub.** This project is configured to ignore it automatically.
*   This tool uses your local machine to send emails securely via Gmail's SMTP server.

---

## 🤝 Contributing
Feel free to fork this project and submit Pull Requests!

## 📄 License
This project is licensed under the MIT License.
