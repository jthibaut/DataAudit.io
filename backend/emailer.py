# backend/emailer.py
import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, To

logger = logging.getLogger("uvicorn.error")

FROM_EMAIL = os.getenv("FROM_EMAIL", "no-reply@dataaudit.io")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

def send_report_email(recipient: str, report_url: str, subject: str = "Votre rapport DataAudit.io"):
    """
    Envoie un email via SendGrid contenant le lien vers le rapport.
    """
    if not SENDGRID_API_KEY:
        raise RuntimeError("SendGrid API key not configured")

    html_content = f"""
    <p>Bonjour,</p>
    <p>Merci pour votre commande. Votre rapport est prêt et disponible ici :</p>
    <p><a href="{report_url}">Télécharger le rapport</a></p>
    <p>Si le lien n'est pas accessible, contactez support@dataaudit.io</p>
    <p>Cordialement,<br/>DataAudit.io</p>
    """

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=recipient,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"SendGrid response: {response.status_code}")
        return response.status_code
    except Exception as e:
        logger.exception("SendGrid send failed")
        raise
