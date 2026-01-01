from flask import Flask, request, render_template
import os
import csv
import io
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_USE_SSL = os.getenv('SMTP_USE_SSL', 'true').lower() in ('1','true','yes')

app = Flask(__name__)


def find_email_and_name(row):
    email = None
    name = ''
    for k, v in row.items():
        if not v:
            continue
        key = k.strip().lower()
        if key in ('email', 'e-mail', 'email_address', 'emailaddress'):
            email = v.strip()
        if key in ('name', 'full_name', 'fullname'):
            name = v.strip()
    return email, name


def send_email(to_email, subject, body, from_addr=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr or SMTP_USER
    msg['To'] = to_email
    msg.set_content(body)

    if SMTP_USE_SSL:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    mode = request.form.get('mode', 'bulk')
    subject = request.form.get('subject', '')
    body_template = request.form.get('body', '')
    from_addr = request.form.get('from_addr') or SMTP_USER

    results = []
    sent = 0
    failed = 0

    if mode == 'single':
        recipient = request.form.get('recipient_email')
        name = request.form.get('recipient_name', '')
        
        if not recipient:
            return 'Recipient email is required for single send mode', 400
            
        # Replace {{name}} even in single mode if name is provided (or empty string)
        body = body_template.replace('{{name}}', name)
        
        try:
            send_email(recipient, subject, body, from_addr)
            results.append((recipient, 'sent'))
            sent += 1
        except Exception as e:
            results.append((recipient, f'error: {e}'))
            failed += 1

    else:
        # Bulk Mode
        uploaded = request.files.get('file')
        if not uploaded or uploaded.filename == '':
            return 'No file uploaded', 400

        stream = io.StringIO(uploaded.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)

        for row in reader:
            email, name = find_email_and_name(row)
            if not email:
                results.append((None, 'missing email'))
                failed += 1
                continue

            body = body_template.replace('{{name}}', name)
            try:
                send_email(email, subject, body, from_addr)
                results.append((email, 'sent'))
                sent += 1
            except Exception as e:
                results.append((email, f'error: {e}'))
                failed += 1

    return render_template('result.html', sent=sent, failed=failed, results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
