import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile,Product

import re

import models