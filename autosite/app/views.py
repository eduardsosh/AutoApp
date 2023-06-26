from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Car, Listing, Image
from .forms import ListingCreationForm

def index(request):
    return render(request, 'listing_list.html', {})
# Create your views here.
def market(request):
    return render(request, 'market.html', {})


def create_listing(request):
    
    form = ListingCreationForm(request.POST, request.FILES)
    if form.is_valid():
        car = Car.objects.create(
            Make=form.cleaned_data['Make'],
            Model=form.cleaned_data['Model'],
            Year=form.cleaned_data['Year'],
            Fuel=form.cleaned_data['Fuel'],
            Engine_cc=form.cleaned_data['Engine_cc'],
            Gearbox=form.cleaned_data['Gearbox'],
            Color=form.cleaned_data['Color'],
        )

        listing = Listing.objects.create(
            Car=car,
            Price=form.cleaned_data['Price'],
            Mileage=form.cleaned_data['Mileage'],
            Location=form.cleaned_data['Location'],
            Description=form.cleaned_data['Description'],
            Phone=form.cleaned_data['Phone'],
            Email=form.cleaned_data['Email'],
            Name=form.cleaned_data['Name'],
        )

        for f in request.FILES.getlist('image'):
            Image.objects.create(
                listing=listing,
                image=f,
            )

        return redirect('listing_list')

    else:
        form = ListingCreationForm()

    return render(request, 'create_listing.html', {'form': form})


def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listing_list.html', {'listings': listings})
