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

# class ClubModelForm(ModelForm):
        
#     class Meta:
#         model = Club
#         fields = '__all__'# we can eithe specify the fields from the model we want to use or
#         exclude = ['club'] # select the ones we want to exclude.
