from django.shortcuts import render,redirect,get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from dataentry import utils
from .models import Subscriber,Email,EmailTracking
from .tasks import send_email_task


# Create your views here.

def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            
            #send email
            mail_subject = request.POST.get("subject")
            message = request.POST.get("body")
            email_list = email_form.email_list
            
            subscribers = Subscriber.objects.filter(email_list=email_list)
            to_email = [email.email_address for email in subscribers]
                       
            attachment = None
            if email_form.attachment:
                attachment = email_form.attachment.path
                
            #handover task to celery
            send_email_task.delay(mail_subject, message, to_email,attachment)
            
            messages.success(request, "Email Sent Successfully!")
            return redirect("send_email")
        else:
            context = {
                "email_form":email_form
            }
            return render(request, "emails/send_email.html" , context)
            
    else:
        
        email_form = EmailForm()
        context = {
            "email_form":email_form
        }
        return render(request, "emails/send_email.html" , context)
    
def track_click(request):
    return 

def track_open(request):
    return 

def track_dashboard(request):
    emails = Email.objects.all()
    context = {
        "emails":emails
    }
    return render(request, "emails/track_dashboard.html", context)

def track_stats(request, pk):
    email = get_object_or_404(Email,pk=pk) 
    context = {
        'email':email
    }
    return render(request, "emails/track_stats.html", context)