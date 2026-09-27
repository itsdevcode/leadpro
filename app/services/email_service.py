from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(to_email: str, otp: str) -> None:
    sender = settings.SMTP_FROM_EMAIL or settings.SMTP_USERNAME
    password = settings.SMTP_PASSWORD
    app_name = settings.PROJECT_NAME

    msg = MIMEMultipart()
    msg["From"] = f"{app_name} <{sender}>"
    msg["To"] = to_email
    msg["Subject"] = f"Your One-Time Password (OTP) - {app_name}"

    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2>Verify Your Email</h2>
        <p>Hello,</p>
        <p>Your one-time password (OTP) for <strong>{app_name}</strong> is:</p>
        <div style="font-size: 24px; font-weight: bold; letter-spacing: 4px; padding: 12px 0; color: #2563eb;">
          {otp}
        </div>
        <p>This OTP is valid for 10 minutes.</p>
        <p>If you did not request this verification, you can safely ignore this email.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;" />
        <p style="font-size: 12px; color: #777;">Thanks,<br>{app_name} Team</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            server.login(settings.SMTP_USERNAME, password)
            server.sendmail(sender, to_email, msg.as_string())
    except Exception as e:
        print(f"Email failed: {e}")
        raise e