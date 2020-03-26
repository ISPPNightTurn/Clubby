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

import re
    
#Model forms: these forms use the models to create themselves basically: (only a single model can't combine multiple.)

class ClubModelForm(ModelForm):
    def clean(self):
        #you can add validation the same way as in a custom form: by adding def clean_field_name(): and raising ValidationError.
        data = self.cleaned_data.get('NIF')
        z = re.match("^[0-9]{8,8}[A-Za-z]$", data)
        print(z == None)
        #check if 8 numbers and a letter with re package
        if(z == None):
            raise ValidationError(_('Invalid NIF - format is 8 numbers and a letter.'))
        return self.cleaned_data
    
    class Meta:
        model = Club
        fields = '__all__'# we can eithe specify the fields from the model we want to use or
        exclude = ['owner'] # select the ones we want to exclude.

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 character max' )
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 character max' )
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    birth_date = forms.DateField(widget=AdminDateWidget(),initial=datetime.date.today,required=True, help_text="Required, your birthday, format: YYYY-MM-DD")

    bio = forms.CharField(max_length=500, required=False, help_text="Optional, tell us something about you.")
    location = forms.CharField(max_length=30, required=False, help_text="Optional, where are you form?.")

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("Sorry that username is already taken :(")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','bio','birth_date','location', 'password1', 'password2')

class ProductModelForm(ModelForm):
    name = forms.CharField(max_length=50, required=True, help_text='Required. 50 character max' )
    price = forms.DecimalField(decimal_places=2,max_digits=5, required=True, help_text='Required. 5 digits max' )
    product_type = forms.CharField(
        max_length=124,
        widget=forms.Select(
            choices=Product.TYPE_OF_PRODUCT,
            attrs={'class': 'browser-default deep-purple darken-4'}
        ),
    )
    reservation_exclusive = forms.BooleanField(required=False,help_text="Is this product exclusive for clients with a reservation?")

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['owner','club'] 

class EventModelForm(ModelForm):
    name = forms.CharField(max_length=50, required=True, help_text='Required. 50 character max' )
    start_date = forms.DateField(widget=AdminDateWidget(),initial=datetime.date.today)
    event_type = forms.CharField(
        max_length=124,
        widget=forms.Select(
            choices=Event.TYPE_OF_EVENT,
            attrs={'class': 'browser-default deep-purple darken-4'}
        ),
    )
    
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['atendees','club'] 


# Custom form we will come back to it later on.

# class EventAddForm(forms.Form):
#     event_date = forms.DateField(help_text="Enter a date between tomorrow and 4 weeks (default 3).")
#     event_time = forms.TimeField(help_text="Your event start time.")
#     event_name = forms.CharField(help_text="The name of the event, this will help users find you!")

#     #these methods exist in the form class and we override them.
#     def clean_event_date(self):
#         #This step gets us the data "cleaned" and sanitized of potentially unsafe input using the default validators
#         data = self.cleaned_data['event_date']

#         # Check if a date is not in the past. 
#         if data < datetime.date.today():
#             # this method of getting text can help us later if we want to translate the site.
#             raise ValidationError(_('Invalid date - event in past'))

#         # Check if a date is in the allowed range (+4 weeks from today).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - event more than 4 weeks ahead'))

#         # Remember to always return the cleaned data.
#         return data