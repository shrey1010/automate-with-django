from django.shortcuts import render
from django.http import HttpResponse
import time
from dataentry.tasks import celery_test_task

def home(request):
    return render(request, "home.html")

def celery_test(request):
    # time consuming task will be executed 
    celery_test_task.delay()    
    return HttpResponse("<h3>Celery function executed successfully!</h3>")