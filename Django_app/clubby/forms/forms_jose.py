import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile,Product, Ticket
from django.utils.translation import gettext

import re

class ProductPurchaseForm(forms.Form):
    quantity = forms.IntegerField(max_value=4,min_value=1,help_text=_("quantity of product you want to buy, max 4."))
    product = forms.IntegerField(widget=forms.HiddenInput())

class RedeemQRCodeForm(forms.Form):
    qr_item_id = forms.IntegerField(widget=forms.HiddenInput())
    
