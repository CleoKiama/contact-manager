from flask import current_app, url_for
from flask_mail import Message
from app import mail
import logging


def send_password_reset_email(user):
    try:
        token = user.get_reset_password_token()
        current_app.logger.info(f"Generated reset token for user {user.email}")

        msg = Message(
            "Reset Your Password",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email],
        )

        reset_url = url_for("auth.reset_password", token=token, _external=True)

        msg.body = f"""To reset your password, visit the following link:
{reset_url}

If you did not request a password reset simply ignore this message.
"""
        current_app.logger.info(f"Attempting to send email to {user.email}")
        mail.send(msg)
        current_app.logger.info(f"Email sent successfully to {user.email}")

    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        raise
