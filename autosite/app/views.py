from django.shortcuts import render
from django.shortcuts import render
from .models import Image
from .forms import ImageForm

def index(request):
    return render(request, 'base.html', {})
# Create your views here.

def market(request):
    return render(request, 'market.html', {})



def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'image_upload.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'image_upload.html', {'form': form})
