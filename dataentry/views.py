from django.shortcuts import render,redirect
from .utils import check_csv_error, get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from .tasks import import_data_task,export_data_task
from django.core.management import call_command
# Create your views here.

def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get("file_path")
        model_name = request.POST.get("model_name")
        
        upload = Upload.objects.create(file=file_path, model_name=model_name)
        relative_path = str(upload.file.url)
        file_path = str(settings.BASE_DIR) + relative_path
        
        #handle errors before assigning task to workers 
        try:
            check_csv_error(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')
        
        # create a celery worker for task 
        import_data_task.delay(file_path, model_name)
        messages.success(request, 'your data is being imported, you will be notified once it is done.')
        return redirect('import_data')
        
    else:
        custom_models = get_all_custom_models()
        context = {
            "models" : custom_models ,
        }
    return render(request, 'dataentry/importdata.html',context=context)

def export_data(request):
    if request.method== "POST":
        
        model_name = request.POST.get("model_name")
        
        export_data_task.delay(model_name)
        messages.success(request, "your data is being exported, you will be notified once it is done.")
        return redirect('export_data')
    else:
        custom_models = get_all_custom_models()
        context= {
             "models" : custom_models ,
        }
        
    return render(request, 'dataentry/exportdata.html', context)