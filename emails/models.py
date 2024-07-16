from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class List(models.Model):
    email_list = models.CharField(max_length=25)
    
    def __str__(self):
        return self.email_list
    
    def count_emails(self):
        count = Subscriber.objects.filter(email_list = self).count()
        return count

class Subscriber(models.Model):
    email_address = models.CharField(max_length=50)
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.email_address
    
class Email(models.Model):
    email_list = models.ForeignKey(List,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = RichTextField()
    attachment = models.FileField(upload_to="email_attachments/",blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
class EmailTracking(models.Model):
    email = models.ForeignKey(Email,on_delete=models.CASCADE,null =True , blank = True)
    subscriber = models.ForeignKey(Subscriber,on_delete=models.CASCADE, null=True , blank = True)
    unique_id = models.CharField(max_length=255,unique=True)
    opened_at = models.DateTimeField(null=True,blank=True)
    clicked_at = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.email
    
class Sent(models.Model):
    email = models.ForeignKey(Email,models.CASCADE,null = True,blank=True)
    total_sent = models.IntegerField(null=True,blank=True)
    
    def __str__( self):
        return str(self.email) + '-' + str(self.total_sent) + ' emails sent'
