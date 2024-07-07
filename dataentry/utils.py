from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import csv 
from django.db import DataError

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