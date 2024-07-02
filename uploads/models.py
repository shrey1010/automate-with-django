from django.db import models

# Create your models here.
class Upload(models.Model):
    file = models.FileField(upload_to="uploads/")
    model_name = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.model_name