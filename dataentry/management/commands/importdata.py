from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError
from dataentry.utils import check_csv_error


class Command(BaseCommand):
    help = "Insert Data Through a CSV"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file")
        parser.add_argument("model", type=str, help="Specify Model")
    
    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_name = kwargs["model"].capitalize()
        
        model = check_csv_error(file_path, model_name)
        
        with open(file_path, "r") as f:
        
            reader = csv.DictReader(f)    
            for row in reader:
                model.objects.create(**row)
                
        self.stdout.write(self.style.SUCCESS("Data Imported Successfully!"))