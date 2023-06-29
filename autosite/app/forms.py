from django import forms
from .models import Car, Listing, Image

from django import forms
from .models import Car, Listing, Image
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class ListingCreationForm(forms.Form):
    FUEL_CHOICES = [
        ('benzīns', _('Benzīns')),
        ('dīzelis', _('Dīzelis')),
        ('elektrība', _('Elektrība')),
        ('benzīns/gāze', _('Benzīns/gāze')),
        ('hibrīds', _('Hibrīds'))
        # Add more options here if necessary
    ]

    GEARBOX_CHOICES = [
        ('automāts', _('Automāts')),
        ('manuāla', _('Manuāla')),
    ]
    
    Make = forms.CharField(max_length=50, label=_('Marka'))
    Model = forms.CharField(max_length=50, label=_('Modelis'))
    Year = forms.IntegerField(label=_('Gads'))
    Fuel = forms.ChoiceField(choices=FUEL_CHOICES, label=_('Degviela'))
    Engine_cc = forms.IntegerField(label=_('Motora tilpums'))
    Gearbox = forms.ChoiceField(choices=GEARBOX_CHOICES, label=_('Ātrumkārba'))
    Color = forms.CharField(max_length=50, label=_('Krāsa'))

    Price = forms.IntegerField(label=_('Cena'))
    Mileage = forms.IntegerField(label=_('Nobraukums'))
    Description = forms.CharField(widget=forms.Textarea, label=_('Apraksts'))
    Phone = forms.CharField(max_length=50, label=_('Tel. nr.'))
    Email = forms.CharField(max_length=50, label=_('Epasts'))
    image = forms.ImageField(label=_('Attēls'))

    def clean_price(self):
        price = self.cleaned_data.get('Price')
        if price is not None and price <= 0:
            raise forms.ValidationError(_('Cenai jābūt pozitīvam skaitlim!'))
        return price


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Epasta adrese'))

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

    


        
