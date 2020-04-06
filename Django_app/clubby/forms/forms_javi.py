import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile, Product, Ticket
from django.utils.translation import gettext

import re

from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

# class TicketCreateModelForm(ModelForm):
#     class Meta:
#         model = CreateTicket
#         fields = '__all__'
#         exclude = ['owner','event','user']

class TicketCreateModelForm(forms.Form):
    def __init__(self, max, *args, **kwargs):
        super(TicketCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['size'] = forms.IntegerField(max_value=max,min_value=1)

    price = forms.DecimalField(decimal_places=2,max_digits=5)#999,99 es el maximo
    category = forms.CharField(max_length = 40, help_text=_('The name of the type of ticket you are trying to sell.'))
    description = forms.CharField(max_length = 40, help_text=_('Decribe what this ticket entices.'), widget=forms.Textarea)
    size = forms.IntegerField(max_value=99999,min_value=1,help_text=_("'Number of tickets. (Max)"))
    


class RatingCreateModelForm(forms.Form):
    stars = forms.IntegerField(max_value=10,min_value=1, help_text=_('Your rating.'))
    text = forms.CharField(max_length = 500, help_text=_('Your oppinion.'), widget=forms.Textarea)
