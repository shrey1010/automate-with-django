
from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import send_email,genrate_csv_file


@app.task
def celery_test_task():
    time.sleep(5)  # simulate a long-running task
    return 'Task Executed Successfully!'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    
    # send email to user 
    to_email = "shreyshukla1010@gmail.com"
    mail_subject = "Import CSV Completed"
    mail_message =  "Your data import task has been successful!"
    send_email(mail_subject, mail_message , to_email)
    
    return "Data Imported Successfully!"


@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e :
        raise e
    
    file_path = genrate_csv_file(model_name)
    
    # send email to user 
    to_email = "shreyshukla1010@gmail.com"
    mail_subject = "Export CSV Completed"
    mail_message =  "Your data export task has been successful!"
    send_email(mail_subject, mail_message , to_email, attachment=file_path)
    
    return "Data Exported Successfully!"