from django.shortcuts import render
from .utils import get_all_custom_models
# Create your views here.

def import_data(request):
    if request.method == "POST":
        pass
    else:
        custom_models = get_all_custom_models()
        context = {
            "models" : custom_models ,
        }
    return render(request, 'dataentry/importdata.html',context=context)