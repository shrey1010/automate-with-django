from django.core.management.base import BaseCommand, CommandError
import csv
# from dataentry.models import Student
from django.apps import apps
import datetime 

class Command(BaseCommand):
    help = "Export Data from Database into a CSV"
    
    def add_arguments(self, parser):
        return parser.add_argument("model_name", type=str, help="Model Name")
    
    def handle(self, *args, **kwargs):
        
        model_name = kwargs["model_name"].capitalize()
        model = None
        
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_label=app_config.name, model_name=model_name)
                break
            except LookupError:
                continue
        
        if model is None:
            raise CommandError(f"{model_name} not found")
            return
                
        data_object = model.objects.all()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f'{model_name}_{timestamp}.csv'
        
        with open(file_path, "w", newline='') as f:
            writer = csv.writer(f)
            
            #write csv Header
            writer.writerow([field.name for field in model._meta.fields])
            
            for data in data_object:
                writer.writerow([getattr(data,field.name) for field in model._meta.fields])
                
        self.stdout.write(self.style.SUCCESS("Data Exported Successfully"))
        