import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile,Product, Ticket

import re

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(max_value=4,min_value=1,help_text="tickets you want to buy, max 4.")
    event = forms.IntegerField(widget=forms.HiddenInput())
    category = forms.CharField(max_length=50,widget=forms.HiddenInput())

class FundsForm(forms.Form):
    ammount = forms.IntegerField(max_value=500,min_value=10,help_text="how much of your currency you want to add, max 500, min 10")

class PremiumForm(forms.Form):
    accept = forms.BooleanField(help_text="if you agree with these terms we welcome you to the clubby team!")

class SearchForm(forms.Form):
    query = forms.CharField(help_text="Looking for something?")

class SearchEventForm(forms.Form):
    # query = forms.CharField(help_text="Looking for something?",required=False)
    start_date = forms.DateField(help_text="We will start looking here.")
    end_date = forms.DateField(help_text="We stop looking here.")

    def clean(self):
        current_date = datetime.datetime.now().date()

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if (start_date < current_date):
            raise ValidationError("Date must be further than today.")
        
        if (end_date < start_date):
            raise ValidationError("Date must be bigger or equal to the starting date.")

        return self.cleaned_data
