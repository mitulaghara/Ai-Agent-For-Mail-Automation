# How to Fix Gmail "Username and Password not accepted" Error

If you are seeing **Error 535: 5.7.8 Username and Password not accepted**, it means Google is blocking the connection because you are using your **regular Gmail password**.

Google requires you to use an **App Password** for security.

## 🟢 Step-by-Step Solution

1.  **Go to Google Account Security**
    *   Visit: [https://myaccount.google.com/security](https://myaccount.google.com/security)

2.  **Enable 2-Step Verification**
    *   If "2-Step Verification" is OFF, turn it **ON**.
    *   You cannot create an App Password without this.

3.  **Generate an App Password**
    *   In the search bar at the top of the settings page, type **"App passwords"** and click on it.
    *   (Or navigate to 2-Step Verification > App Passwords at the bottom).
    *   **App name**: Enter "Mail Agent".
    *   Click **Create**.

4.  **Copy the 16-Character Password**
    *   Google will show you a password like `abcd efgh ijkl mnop`.
    *   **Copy this password** (spaces don't matter, but usually you paste it without spaces).

5.  **Update your `.env` file**
    *   Open the `.env` file in your project folder.
    *   Find the `SMTP_PASSWORD` line.
    *   Replace your old password with the new 16-character App Password.
    *   **Save the file**.

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  <-- PUT NEW PASSWORD HERE
SMTP_USE_SSL=true
```

6.  **Restart the App**
    *   Stop the current server (Ctrl+C).
    *   Run it again: `python app.py`.

Now your emails will send successfully! 🚀
