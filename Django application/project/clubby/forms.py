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

from clubby.models import Club, Event, Profile

import re
    
#Model forms: these forms use the models to create themselves basically: (only a single model can't combine multiple.)

class ClubModelForm(ModelForm):
    class Meta:
        model = Club
        fields = '__all__'# we can eithe specify the fields from the model we want to use or
        exclude = ['owner'] # select the ones we want to exclude.

#you can add validation the same way as in a custom form: by adding def clean_field_name(): and raising ValidationError.
    def clean_NIF(self):
        data = self.cleaned_data.get('NIF')

        #check if 8 numbers and a letter with re package
        if((re.match("^[0-9]{8,8}[A-Za-z]$"), data) == None):
            raise ValidationError(_('Invalid NIF - format is 8 numbers and a letter.'))
        return data

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


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