# same as dp forms they are used for handling form data:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# this guide provides very usefull information for form development.
import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile, Product, Ticket
from django.contrib.admin.widgets import AdminDateWidget
from decimal import Decimal
from django.utils.translation import gettext

import re

class DateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('placeholder', 'jj/mm/aaaa')
        super().__init__(*args, **kwargs)
    
#Model forms: these forms use the models to create themselves basically: (only a single model can't combine multiple.)

class ClubModelForm(ModelForm):
    def clean(self):
        #you can add validation the same way as in a custom form: by adding def clean_field_name(): and raising ValidationError.
        data = self.cleaned_data.get('NIF')
        z = re.match("^[0-9]{8,8}[A-Za-z]$", data)
        #check if 8 numbers and a letter with re package
        if(z == None):
            raise ValidationError(_('Invalid NIF - format is 8 numbers and a letter.'))
        return self.cleaned_data
    
    class Meta:
        model = Club
        fields = '__all__'# we can eithe specify the fields from the model we want to use or
        exclude = ['owner'] # select the ones we want to exclude.

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text=_('Required. 30 character max') )
    last_name = forms.CharField(max_length=30, required=True, help_text=_('Required. 30 character max' ))
    email = forms.EmailField(max_length=254, required=True, help_text=_('Required. Inform a valid email address.'))

    birth_date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker'}), initial= (datetime.datetime.now()-datetime.timedelta(days=365*18)).date())
    
    bio = forms.CharField(max_length=500, required=False, help_text=_("Optional, tell us something about you."))
    location = forms.CharField(max_length=30, required=False, help_text=_("Optional, where are you form?."))

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        birth_date = self.cleaned_data.get('birth_date')

        if(birth_date > (datetime.datetime.now()-datetime.timedelta(days=365*18)).date()):
            raise ValidationError(_("You're too young. You must be 18 or older to use this app."))
        
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Email exists"))
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("Sorry that username is already taken :("))

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'bio', 'location', 'password1', 'password2')

class ProductModelForm(ModelForm):
    name = forms.CharField(max_length=50, required=True, help_text=_('Required. 50 character max' ))
    price = forms.DecimalField(decimal_places=2,max_digits=5, required=True, min_value=Decimal('0.00'), help_text=_('Required. 5 digits max') )

    TYPE_OF_PRODUCT = (
        ('r', _('refreshment')),
        ('c', _('cocktail')),
        ('s', _('shot')),
        ('b', _('beer')),
        ('w', _('wine')),
        ('k', _('snack')),
        ('h', _('hookah')),
        ('m', _('misc.')),
    )
    product_type = forms.CharField(
        max_length=124,
        widget=forms.Select(
            choices=Product.TYPE_OF_PRODUCT,
            attrs={'class': 'browser-default deep-purple darken-4'}
        ),
    )
    reservation_exclusive = forms.BooleanField(required=False,help_text=_("Is this product exclusive for clients with a reservation?"))

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['owner','club'] 

class EventModelForm(ModelForm):
    name = forms.CharField(max_length=50, required=True, help_text=_('Required. 50 character max' ))
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker'}), initial= datetime.date.today)

    event_type = forms.CharField(
        max_length=100,
        widget=forms.Select(
            choices=Event.TYPE_OF_MUSIC,
            attrs={'class': 'browser-default deep-purple darken-4'}
        ),
    )

    start_time = forms.IntegerField(
        widget=forms.Select(
            choices=Event.START_TIMES,
            attrs={'class': 'browser-default deep-purple darken-4'}
        ),
    )

    duration = forms.IntegerField(
        widget=forms.Select(
            choices=Event.DURATIONS,
            attrs={'class': 'browser-default deep-purple darken-4'}
        ),
    )


    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['atendees','club'] 

class SpotifyForm(forms.Form):
    spotify_username = forms.CharField(max_length=60, help_text=_("your spotify username, you will be prompted for authorization"))