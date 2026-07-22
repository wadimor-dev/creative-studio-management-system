import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Optional, List
from app.core.notification.channels.base import NotificationChannelBase
from app.core.notification.models import Notification
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailChannel(NotificationChannelBase):
    @property
    def channel_type(self) -> str:
        return "email"

    async def send(self, notification: Notification, context: Any = None) -> bool:
        user_email = self._get_user_email(notification)
        if not user_email:
            logger.warning("No email found for user %s", notification.user_id)
            return False

        html_body = self._render_html(notification.title, notification.body)

        try:
            self._send_email_smtp(
                to_email=user_email,
                subject=notification.title,
                html_body=html_body,
            )
            return True
        except Exception:
            logger.exception("Failed to send email notification to %s", user_email)
            return False

    def _get_user_email(self, notification: Notification) -> Optional[str]:
        user = notification.user
        if user and hasattr(user, "email"):
            return user.email
        return None

    def _render_html(self, title: str, body: Optional[str]) -> str:
        escaped_body = (body or "").replace("\n", "<br>")
        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px">
<div style="max-width:600px;margin:0 auto;background:#fff;border-radius:8px;border:1px solid #e5e7eb">
<div style="padding:24px;border-bottom:1px solid #e5e7eb">
<h2 style="margin:0;color:#111827;font-size:18px">{title}</h2>
</div>
<div style="padding:24px;color:#374151;font-size:14px;line-height:1.6">
{escaped_body}
</div>
<div style="padding:16px 24px;border-top:1px solid #e5e7eb;font-size:12px;color:#9ca3af;text-align:center">
<p style="margin:0">{settings.APP_NAME} &mdash; {settings.APP_ENV}</p>
</div>
</div>
</body>
</html>"""

    def _send_email_smtp(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> None:
        if not settings.SMTP_HOST:
            logger.warning("SMTP not configured, skipping email to %s", to_email)
            return

        msg = MIMEMultipart("alternative")
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject

        if cc:
            msg["Cc"] = ", ".join(cc)

        msg.attach(MIMEText(html_body, "html"))

        recipients = [to_email] + (cc or []) + (bcc or [])

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, recipients, msg.as_string())

        logger.info("Email sent to %s: %s", to_email, subject)
