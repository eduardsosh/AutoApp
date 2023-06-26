from django import forms
from .models import Car, Listing, Image

from django import forms
from .models import Car, Listing, Image

class ListingCreationForm(forms.Form):
    Make = forms.CharField(max_length=50)
    Model = forms.CharField(max_length=50)
    Year = forms.IntegerField()
    Fuel = forms.CharField(max_length=50)
    Engine_cc = forms.IntegerField()
    Gearbox = forms.CharField(max_length=50)
    Color = forms.CharField(max_length=50)

    Price = forms.IntegerField()
    Mileage = forms.IntegerField()
    Location = forms.CharField(max_length=50)
    Description = forms.CharField(widget=forms.Textarea)
    Phone = forms.CharField(max_length=50)
    Email = forms.CharField(max_length=50)
    Name = forms.CharField(max_length=50)
    
    image = forms.ImageField()
    


        
