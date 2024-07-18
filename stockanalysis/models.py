from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    sector = models.CharField(max_length=100 , null=True, blank=True)
    exchange = models.CharField(max_length=100)
    country = models.CharField(max_length=50,null=True, blank=True)
    
    def __str__(self):
        return self.name