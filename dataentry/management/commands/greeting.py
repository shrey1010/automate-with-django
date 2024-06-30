from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help= "Greets the user"
    
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help="User Name")
    
    def handle(self, *args, **kwargs):
        name = kwargs.get("name")
        greeting = f"Hi {name} Good Morning!"
        self.stdout.write(greeting) 
        # self.stderr.write(greeting)    makes red color of text to print the error 
        # self.stdout.write(self.style.SUCCESS(greeting))  makes green color of text 