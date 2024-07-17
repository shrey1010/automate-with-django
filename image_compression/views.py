from django.shortcuts import render
from .forms import CompressImageForm
# Create your views here.

def compress(request):
    form = CompressImageForm()
    context = {
        "form":form,
    }
    return render(request, "image_compression/compress.html",context=context)