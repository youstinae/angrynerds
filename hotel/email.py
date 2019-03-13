from flask import current_app
from flask_mail import Message


def send_async_email(msg):
    with current_app.app_context():
        current_app.mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    current_app.mail.send(msg)


def notify_register_account():
    subject = 'New account registration'
    sender = 'royal.hotel@localhost.com'
    recipients = ["gharzedd@mail.usf.edu"]
    text_body = 'your account is setup please confirm'
    html_body = True
    send_email(subject=subject,
               sender=sender,
               recipients=recipients,
               text_body=text_body,
               html_body=html_body)


def notify_confirm_account():
    pass


def notify_recover_username():
    pass


def notify_recover_password():
    pass
