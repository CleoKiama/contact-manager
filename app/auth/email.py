from flask import current_app, url_for
import resend


def send_password_reset_email(user):
    try:
        token = user.get_reset_password_token()
        current_app.logger.info(f"Generated reset token for user {user.email}")

        resend.api_key = current_app.config["RESEND_API_KEY"]
        reset_url = url_for("auth.reset_password", token=token, _external=True)

        email = resend.Emails.send(
            {
                "from": current_app.config["MAIL_DEFAULT_SENDER"],
                "to": user.email,
                "subject": "Reset Your Password",
                "html": f"""
                <html>
                <body>
                    <h1>Password Reset Request</h1>
                    <p>To reset your password, visit the following link:</p>
                    <p><a href="{reset_url}">{reset_url}</a></p>
                    <p>If you did not request a password reset, please ignore this message.</p>
                    <p>This link will expire in 60 minutes.</p>
                </body>
                </html>
            """,
            }
        )

        current_app.logger.info(f"Email sent successfully to {user.email}")
        return email

    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        raise
