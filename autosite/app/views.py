# Main views for the app
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Database
from .models import Car, Listing, Image
from .forms import ListingCreationForm

# Register and Login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

from django.core.paginator import Paginator

def index(request):
    return redirect('listing_list')
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
    listings = Listing.objects.all().prefetch_related('image_set')
    paginator = Paginator(listings, 12) # Show 12 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'listing_list.html', {'listings': page_obj})
    #return render(request, 'listing_list.html', {'listings': listings})

def delete_all_listings(request):
    cars = Car.objects.all()
    listings = Listing.objects.all()
    for listing in listings:
        for image in listing.image_set.all():
            image.delete()
        listing.delete()
        
    for car in cars:
        car.delete()
        
    return redirect('listing_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('listing_list')  # Redirect to a success page.
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('listing_list') # Or specify the name of your home view
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('listing_list')  # Or specify the name of your home view