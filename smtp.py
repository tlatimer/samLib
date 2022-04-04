import smtplib
from email.message import EmailMessage

toEmails = ', '.join([
    'user1@example.org',
    # 'user2@example.org',
])

msg = EmailMessage()
msg['Subject'] = 'subject'
msg['From'] = 'user3@example.org'
msg['To'] = toEmails

msg.set_content('Body')

with smtplib.SMTP('8.8.8.8') as smtp:
    smtp.send_message(msg)
