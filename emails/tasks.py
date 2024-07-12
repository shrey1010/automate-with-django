from awd_main.celery import app
from dataentry.utils import send_email

@app.task
def send_email_task(mail_subject, message, to_email,attachment):
    send_email(mail_subject, message, to_email,attachment)
    return 'Email Send Successfuly!'