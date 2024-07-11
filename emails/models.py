from django.db import models

# Create your models here.

class List(models.Model):
    email_list = models.CharField(max_length=25)
    
    def __str__(self):
        return self.email_list
    
class Subscriber(models.Model):
    email_address = models.CharField(max_length=50)
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.email_address
    
class Email(models.Model):
    email_list = models.ForeignKey(List,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    attachment = models.FileField(upload_to="email_attachments/")
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
