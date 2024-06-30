from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv


class Command(BaseCommand):
    help = "Insert Data Through a CSV"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file")
        parser.add_argument("model", type=str, help="Specify Model")
    
    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_name = kwargs["model"].capitalize()
        model=None
        #search model in project
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_label=app_config.label, model_name= model_name)
                break
            except LookupError:
                continue # model not found in first app keep searching in next app
            
        if not model:
            raise CommandError(f" Model {model_name} not found in any app!")
        
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                model.objects.create(
                    **row
                )
        self.stdout.write(self.style.SUCCESS("Data Imported Successfully!"))