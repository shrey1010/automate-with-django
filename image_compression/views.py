from django.shortcuts import render,redirect
from .forms import CompressImageForm
from PIL import Image   
import io
from django.http import HttpResponse
# Create your views here.

def compress(request):
    if request.method == "POST":
        user = request.user
        form = CompressImageForm(request.POST,request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data["original_img"]
            quality = form.cleaned_data["quality"]
            
            compressed_image = form.save(commit=False)
            compressed_image.user = user
            
            #perform compression 
            img = Image.open(original_img)
            img_format = img.format
            buffer = io.BytesIO()   # its a empty byte sequence to store 
            img.save(buffer, format=img_format, quality=quality)
            buffer.seek(0)
            
            compressed_image.compressed_img.save(f"compressed_{original_img}",buffer)
            
            # download compressed image
            response = HttpResponse(buffer.getvalue(),content_type=f"image/{img_format.lower()}")
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
            return response
            
        else:
            context = {
                "form":form,
            }
            return render(request, "image_compression/compress.html",context=context)
        return 
    else:
        form = CompressImageForm()
        context = {
            "form":form,
        }
        return render(request, "image_compression/compress.html",context=context)