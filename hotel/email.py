from flask import current_app, flash
from flask_mail import Mail, Message

mail = Mail()


def send_async_email(msg):
    try:
        with current_app.app_context():
            mail.send(msg)
    except BaseException as e:
        flash('error %s' % e)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject=subject,
                  sender='royal.hotel@localhost.com', recipients=to)

#     msg.body = render_template('email/%s.txt' % template, **kwargs)
#     msg.html = render_template('email/%s.html' % template, **kwargs)
    msg.body = 'Your account is registered'
    msg.html = 'Your account is registered'
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    current_app.mail.send(msg)


def notify_register_account():
    subject = 'New account registration'
    recipients = ["gharzedd@mail.usf.edu"]

    send_mail(to=recipients,
              subject=subject,
              template='notify_register')


def notify_confirm_account():
    pass


def notify_recover_username():
    pass


def notify_recover_password():
    pass
