from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import csv 
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os 
from emails.models import Email,Sent
from emails.models import EmailTracking,Subscriber
import hashlib
import time
from bs4 import BeautifulSoup

def get_all_custom_models():
    
    default_models = ['LogEntry','Permission','Group','ContentType','Session','Upload']
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
        
    return custom_models

def check_csv_error(file_path, model_name):
    model=None
    #search model in project
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_label=app_config.label, model_name= model_name)
            break
        except LookupError:
            continue # model not found in first app keep searching in next app
        
    if not model:
        raise CommandError(f"Model {model_name} not found in any app!")
    
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        
    try:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            csv_header = reader.fieldnames
            
            if csv_header!= model_fields:
                raise DataError(f"CSV file Doesn't match with the {model_name} table fields")
        
    except Exception as e:
        raise e 
        
    return model

def send_email(mail_subject, message , to_email, attachment = None, email_id = None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        if isinstance(to_email, str):
            to_email = [to_email]
        
        for recipient_email in to_email:
            # create email tracking record
            mail_message = message
            if email_id: 
                
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list = email.email_list, email_address = recipient_email) 
                
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                
                email_tracking = EmailTracking.objects.create(
                email = email,
                subscriber = subscriber,
                unique_id = unique_id,
                )
                
                # genrate tracking pixel
                base_url = settings.BASE_URL
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
                
                #search for  link in email body
                soup = BeautifulSoup(mail_message,"html.parser")
                urls = [url['href'] for url in soup.find_all('a',href=True)]               
                
                # if link found in body will inject unique id in that
                for url in urls:
                    tracking_url = f"{click_tracking_url}?url={url}"
                    mail_message = mail_message.replace(f"{url}", f"{tracking_url}")
                
                #create email with tracking pixel image
                open_tracking_image = f"<img src='{open_tracking_url}' width='1' height='1'>"
                mail_message += open_tracking_image
                    
            mail= EmailMessage(mail_subject, mail_message, from_email,to=[recipient_email])
            if attachment is not None:
                mail.attach_file(attachment)
            mail.content_subtype = "html"
            mail.send()
        
        if email_id is not None:
            email = Email.objects.get(pk=email_id)
            sent = Sent.objects.create(
                email = email,
                total_sent = email.email_list.count_emails()
            )
    
    except Exception as e:
        raise e
    
    
    
def genrate_csv_file(model_name):
    
    export_dirs = 'exported_data'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    file_name = f'{model_name}_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dirs, file_name)
    return file_path