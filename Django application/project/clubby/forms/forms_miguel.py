import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile,Product

import re

# class ClubModelForm(ModelForm):
        
#     class Meta:
#         model = Club
#         fields = '__all__'# we can eithe specify the fields from the model we want to use or
#         exclude = ['club'] # select the ones we want to exclude.
