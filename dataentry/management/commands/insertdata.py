from django.core.management.base import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):
    help="It Will Insert Data Into Database"
    
    def handle(self, *args, **kwargs):
        
        dataset = [
            {'roll_no':"1002","name":"palak","age":20},
            {'roll_no':"1003","name":"shivam","age":20},
            {'roll_no':"1004","name":"vallabh","age":20}
        ]
        
        for data in dataset:
            
            roll_no = data["roll_no"]
            exists = Student.objects.filter(roll_no=roll_no).exists()
            if not exists:
                Student.objects.create(
                    roll_no=data["roll_no"],
                    name=data["name"],
                    age=data["age"]
                )
        self.stdout.write(self.style.SUCCESS("Data Inserted Successfully!"))