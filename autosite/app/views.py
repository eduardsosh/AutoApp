# Main views for the app
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connections
import json

from django.contrib.auth.decorators import user_passes_test

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Database
from .models import Car, Listing, Image , Bookmark
from .forms import ListingCreationForm
from .forms import EditUserForm
from .forms import RegistrationForm

# Register and Login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

# Listing list, filter and search
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Min, Max


def index(request):
    return redirect('listing_list')
# Create your views here.
def market(request):
    return render(request, 'market.html', {})

@login_required
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
            Location="None",
            Description=form.cleaned_data['Description'],
            Phone=form.cleaned_data['Phone'],
            Email=form.cleaned_data['Email'],
            Name="None",
            Link="",  # Initially set Link to an empty string
            User=request.user,
        )

        # Set Link to the URL of the listing
        listing.Link = request.build_absolute_uri(listing.get_absolute_url())
        listing.save()

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
    query_params = request.GET.copy()
    
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    fuel = request.GET.get('fuel')
    gearbox = request.GET.get('gearbox')
    color = request.GET.get('color')
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order')
    only_bookmarks = request.GET.get('only_bookmarks')
    only_owned = request.GET.get('only_owned')

    listings = Listing.objects.all().select_related('Car')

    if query or min_price or max_price or min_year or max_year or fuel or gearbox or color or sort_by or order or only_bookmarks or only_owned:
        if query:
            listings = listings.filter(
                Q(Description__icontains=query) |
                Q(Car__Make__icontains=query) |
                Q(Car__Model__icontains=query)
            )

        if min_price:
            listings = listings.filter(Price__gte=min_price)

        if max_price:
            listings = listings.filter(Price__lte=max_price)

        if min_year:
            listings = listings.filter(Car__Year__gte=min_year)

        if max_year:
            listings = listings.filter(Car__Year__lte=max_year)

        if fuel:
            listings = listings.filter(Car__Fuel=fuel)

        if gearbox:
            listings = listings.filter(Car__Gearbox=gearbox)

        if color:
            listings = listings.filter(Car__Color=color)

        if only_bookmarks:
            bookmark_ids = Bookmark.objects.filter(user=request.user).values_list('listing', flat=True)
            listings = listings.filter(id__in=bookmark_ids)
        
        if only_owned:
            owned_ids = Listing.objects.filter(User=request.user).values_list('id', flat=True)
            listings = listings.filter(id__in=owned_ids)

        if sort_by and order:
            if order == 'asc':
                listings = listings.order_by(sort_by)
            elif order == 'desc':
                listings = listings.order_by(f'-{sort_by}')
    else:
        if 'random_order' not in request.session:
            listings = listings.order_by('?')
            request.session['random_order'] = [item.id for item in listings]
        else:
            listings = listings.filter(id__in=request.session['random_order'])

    # Retrieve available options for fuel, gearbox, and color
    fuel_options = Car.objects.values_list('Fuel', flat=True).distinct()
    gearbox_options = Car.objects.values_list('Gearbox', flat=True).distinct()
    color_options = Car.objects.values_list('Color', flat=True).distinct()

    # Get min and max year values for the range input
    min_year_value = Car.objects.aggregate(Min('Year'))['Year__min']
    max_year_value = Car.objects.aggregate(Max('Year'))['Year__max']

    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    if request.user.is_authenticated:
        bookmarked_listing_ids = Bookmark.objects.filter(user=request.user).values_list('listing_id', flat=True)
        owned_listing_ids = Listing.objects.filter(User=request.user).values_list('User', flat=True)
    else:
        bookmarked_listing_ids = []
        owned_listing_ids = []



    return render(
        request,
        'listing_list.html',
        {
            'listings': page_obj,
            'fuel_options': fuel_options,
            'gearbox_options': gearbox_options,
            'color_options': color_options,
            'min_year_value': min_year_value,
            'max_year_value': max_year_value,
            'query_params': query_params,
            'bookmarked_listing_ids': bookmarked_listing_ids,
            'owned_listing_ids': owned_listing_ids,
        }
    )

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

from django.http import HttpResponseForbidden

def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Check if the user is either a staff member or the creator of the listing
    if request.user.is_staff or request.user == listing.User:
        listing.delete()
        return redirect('listing_list')

    # If the user is neither a staff member nor the creator of the listing, return a forbidden response
    return HttpResponseForbidden("You are not allowed to delete this listing.")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('listing_list')  # Redirect to a success page.
    else:
        form = RegistrationForm()
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

def edit_user(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('listing_list') # Or specify the name of your home view
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

from django.shortcuts import get_object_or_404

def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    return render(request, 'listing_detail.html', {'listing': listing})

@csrf_exempt
@login_required
def bookmark(request):
    listing_id = json.loads(request.body).get('listing_id')

    bookmark, created = Bookmark.objects.get_or_create(user=request.user, listing_id=listing_id)

    if not created:
        bookmark.delete()
        return JsonResponse({ 'bookmarked': False })
    else:
        return JsonResponse({ 'bookmarked': True })
