from flask import render_template, current_app
from flask_mail import Message
from app import mail
from flask import url_for


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message(
        "Reset Your Password",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
    )

    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not request a password reset, simply ignore this message.
"""

    msg.html = f"""
<p>To reset your password, visit the following link:</p>
<p><a href="{url_for('auth.reset_password', token=token, _external=True)}">
    Click here to reset your password
</a></p>
<p>If you did not request a password reset, simply ignore this message.</p>
"""

    mail.send(msg)
