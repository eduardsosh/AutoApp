from django import forms
from .models import Car, Listing, Image

from django import forms
from .models import Car, Listing, Image
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class ListingCreationForm(forms.Form):
    FUEL_CHOICES = [
        ('benzīns', 'Benzīns'),
        ('dīzelis', 'Dīzelis'),
        ('elektrība', 'Elektrība'),
        ('benzīns/gāze', 'Benzīns/gāze'),
        ('hibrīds', 'Hibrīds')
        # Add more options here if necessary
    ]
    
    GEARBOX_CHOICES = [
        ('automāts', 'Automāts'),
        ('manuāla', 'Manuāla'),]
    
    Make = forms.CharField(max_length=50)
    Model = forms.CharField(max_length=50)
    Year = forms.IntegerField()
    Fuel = forms.ChoiceField(choices=FUEL_CHOICES)
    Engine_cc = forms.IntegerField()
    Gearbox = forms.ChoiceField(choices=GEARBOX_CHOICES)
    Color = forms.CharField(max_length=50)

    Price = forms.IntegerField()
    Mileage = forms.IntegerField()
    Description = forms.CharField(widget=forms.Textarea)
    Phone = forms.CharField(max_length=50)
    Email = forms.CharField(max_length=50)
    image = forms.ImageField()
    
    
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Email Address'))

    password1 = forms.CharField(
        label=_("Parole"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Ievadiet drošu paroli!"),
    )

    password2 = forms.CharField(
        label=_("Parole vēlreiz"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Ievadiet paroli vēlreiz!"),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name","password1", "password2"]
        labels = {
            'username': _('Lietotājvārds'),
            'email': _('E-pasts'),
            'first_name': _('Vārds'),
            'last_name': _('Uzvārds'),
            'password1': _('Parole'),
            'password2': _('Parole vēlreiz'),
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username" , 'first_name', 'last_name']
        # Add any other fields you want to include.

    


        
