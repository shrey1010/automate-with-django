from django.core.management.base import BaseCommand
import csv
from dataentry.models import Student
import datetime 

class Command(BaseCommand):
    help = "Export Data into a CSV"
    
    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f'students_data{timestamp}.csv'
        
        with open(file_path, "w",newline='') as f:
            writer = csv.writer(f)
            
            #write csv Header
            writer.writerow(["Roll NO","Name","Age"])
            for student in students:
                writer.writerow([student.roll_no, student.name, student.age])
                
        self.stdout.write(self.style.SUCCESS("Data Exported Successfully"))
        