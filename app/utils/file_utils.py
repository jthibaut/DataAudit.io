import os


def save_uploaded_file(uploaded_file, target_dir: str) -> str:
    os.makedirs(target_dir, exist_ok=True)
    filename = uploaded_file.name
    output_path = os.path.join(target_dir, filename)
    with open(output_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return output_path
```

---

### FILE: app/utils/email_utils.py
```python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "no-reply@dataaudit.io")


def send_report_email(to_email: str, subject: str, body: str, attachment_path: str = None):
    if not SENDGRID_API_KEY:
        raise RuntimeError("SendGrid API key not set. Configure SENDGRID_API_KEY in .env")

    message = Mail(from_email=FROM_EMAIL, to_emails=to_email, subject=subject, html_content=body)

    if attachment_path:
        # For MVP we skip attachment encoding complexity — instead include a hosted link in body after you implement storage
        pass

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        raise e