from flask import current_app, flash
from flask_mail import Mail, Message

mail = Mail()


def send_email_async(msg):
    try:
        with current_app.app_context():
            mail.send(msg)
    except BaseException as e:
        flash('error %s' % e)


def send_email(to, subject, template):
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
