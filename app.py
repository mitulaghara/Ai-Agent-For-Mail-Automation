from flask import Flask, request, render_template, Response, stream_with_context
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

    # 1. Prepare list of recipients
    recipients = []

    if mode == 'single':
        r_email = request.form.get('recipient_email')
        r_name = request.form.get('recipient_name', '')
        if not r_email:
            return 'Recipient email is required for single send mode', 400
        recipients.append({'email': r_email, 'name': r_name})
    else:
        # Bulk Mode
        uploaded = request.files.get('file')
        if not uploaded or uploaded.filename == '':
            return 'No file uploaded', 400

        try:
            stream = io.StringIO(uploaded.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            for row in reader:
                email, name = find_email_and_name(row)
                if email:
                    recipients.append({'email': email, 'name': name})
        except Exception as e:
            return f"Error reading CSV file: {e}", 400

    if not recipients:
        return "No valid recipients found.", 400

    # 2. Generator Function for Streaming Response
    def generate():
        total = len(recipients)
        sent = 0
        failed = 0

        # Yield HTML Header
        yield render_template('parts/header.html', total=total)

        # Process Each Recipient
        for r in recipients:
            email = r['email']
            name = r['name']
            status = 'pending'

            # Personalize Body
            body = body_template.replace('{{name}}', name)

            # Send Email
            try:
                send_email(email, subject, body, from_addr)
                status = 'sent'
                sent += 1
            except Exception as e:
                # Log error safely
                status = str(e)
                failed += 1

            # Yield Table Row with Status
            yield render_template('parts/row.html', email=email, status=status, sent_count=sent, failed_count=failed)

        # Yield HTML Footer
        yield render_template('parts/footer.html', sent=sent, failed=failed)

    # 3. Return Streaming Response
    return Response(stream_with_context(generate()))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
