from threading import Thread
from flask_mail import Message
from resources.errors import InternalServerError

def send_async_email(app, msg):
    from app import mail
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working")


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    from app import app
    Thread(target=send_async_email, args=(app, msg)).start()