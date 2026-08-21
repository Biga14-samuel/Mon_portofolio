import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.config import get_settings
import smtplib
from email.message import EmailMessage

s = get_settings()
print('Using SMTP server:', s.smtp_server, 'port:', s.smtp_port)
print('SMTP user:', s.smtp_user)
print('SMTP recipient:', s.smtp_recipient)

msg = EmailMessage()
msg.set_content('Test d\'envoi SMTP depuis le script de vérification.')
msg['Subject'] = 'Test SMTP'
msg['From'] = s.smtp_user
msg['To'] = s.smtp_recipient
msg['Reply-To'] = s.smtp_user

try:
    if s.smtp_port == 465:
        with smtplib.SMTP_SSL(s.smtp_server, s.smtp_port, timeout=30) as server:
            server.login(s.smtp_user, s.smtp_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(s.smtp_server, s.smtp_port, timeout=30) as server:
            if server.has_extn('STARTTLS'):
                server.starttls()
            server.login(s.smtp_user, s.smtp_password)
            server.send_message(msg)
    print('Email envoyé avec succès')
except Exception as exc:
    print('Erreur lors de l\'envoi :', repr(exc))
    raise
