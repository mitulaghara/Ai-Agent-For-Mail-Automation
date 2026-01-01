import os
import csv
import argparse
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_USE_SSL = os.getenv('SMTP_USE_SSL', 'true').lower() in ('1','true','yes')


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


def main():
    parser = argparse.ArgumentParser(description='Send bulk emails from CSV')
    parser.add_argument('csvfile')
    parser.add_argument('--subject', required=True)
    parser.add_argument('--body', required=True)
    parser.add_argument('--from', dest='from_addr')
    args = parser.parse_args()

    with open(args.csvfile, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email, name = find_email_and_name(row)
            if not email:
                print('Skipping row, no email')
                continue
            body = args.body.replace('{{name}}', name)
            try:
                send_email(email, args.subject, body, args.from_addr)
                print('Sent to', email)
            except Exception as e:
                print('Failed', email, e)


if __name__ == '__main__':
    main()
