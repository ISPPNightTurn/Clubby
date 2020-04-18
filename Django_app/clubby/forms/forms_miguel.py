import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError

from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from clubby.models import Club, Event, Profile, Product, Ticket
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext

import re


class DateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('placeholder', 'jj/mm/aaaa')
        super().__init__(*args, **kwargs)


class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(
        max_value=4, min_value=1, help_text=_("tickets you want to buy, max 4."))
    event = forms.IntegerField(widget=forms.HiddenInput())
    category = forms.CharField(max_length=50, widget=forms.HiddenInput())


class FundsForm(forms.Form):
    ammount = forms.DecimalField(decimal_places=2,max_value=500, min_value=10, help_text=_("how much of your currency you want to add, max 500€, min 10€"))
    ammount.widget.attrs.update({'placeholder': '0.00'})
class PremiumForm(forms.Form):
    accept = forms.BooleanField(help_text=_("if you agree with these terms we welcome you to the clubby team!"))


class SearchForm(forms.Form):
    query = forms.CharField(help_text=_("Looking for something?"))


class SearchEventForm(forms.Form):
    # query = forms.CharField(help_text="Looking for something?",required=False)
    start_date = forms.DateField(widget=AdminDateWidget(attrs={'class': 'datepicker inicio'}), help_text=_("We will start looking here."))
    end_date = forms.DateField(widget=AdminDateWidget(attrs={'class': 'datepicker fin'}), help_text=_("We stop looking here."))

    def clean(self):
        current_date = datetime.datetime.now().date()

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if (start_date < current_date):
            raise ValidationError(_("Date must be further than today."))

        if (end_date < start_date):
            raise ValidationError(
                _("Date must be bigger or equal to the starting date."))

        return self.cleaned_data


class EditProfileForm(forms.Form):
    # we override the init object to allow the request to get here.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=30, required=True, help_text=_('Required. 30 character max'))
    last_name = forms.CharField(max_length=30, required=True, help_text=_('Required. 30 character max'))
    email = forms.EmailField(max_length=254, help_text=_('Required. Inform a valid email address.'))
    bio = forms.CharField(max_length=500, required=False, help_text=_("Optional, tell us something about you."))
    location = forms.CharField(max_length=30, required=False, help_text=_("Optional, where are you form?."))    
    birth_date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker'}))
    picture = forms.URLField(help_text=_("URL to a picture of your pretty face (200 characters max)"), required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        birth_date = self.cleaned_data.get('birth_date')

        try:
            user_with_mail = User.objects.filter(email=email)[0]
        except:
            user_with_mail = None
        if ((user_with_mail != None) and (user_with_mail != self.request.user)):
            raise ValidationError(_("Email exists"))

        if(birth_date > (datetime.datetime.now()-datetime.timedelta(days=365*18)).date()):
            raise ValidationError(_("You're too young. You must be 18 or older to use this app."))

        return self.cleaned_data
