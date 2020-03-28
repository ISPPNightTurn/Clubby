import datetime

from django.test import TestCase
from django.utils import timezone

from clubby.forms import ClubModelForm



# these tests are part of the following tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

#######################
#    CLUBBY TESTS     #
#######################

class ClubModelFormTests(TestCase):
    def test_form_complete(self):
        form_data = {'name': 'name', 'address': 'address', 'max_capacity': 10, 'NIF': '12345678x', 'picture': 'https://picture.com'}
        form = ClubModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form(self):
        form_data = {'name': 'name', 'address': 'address', 'max_capacity': 10, 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_name_too_big(self):
        form_data = {'name': 'namenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamenamename',
            'address': 'address', 'max_capacity': 10, 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_name_null(self):
        form_data = {'address': 'address', 'max_capacity': 10, 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_address_too_big(self):
        form_data = {'name': 'name','address': 'addressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddressaddress',
        'max_capacity': 10, 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_address_null(self):
        form_data = {'name': 'name', 'max_capacity': 10, 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_max_capacity_neg(self):
        form_data = {'name': 'name', 'address': 'address', 'max_capacity': -1, 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_max_capacity_null(self):
        form_data = {'name': 'name','address': 'address', 'NIF': '12345678x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_NIF_7_numbers(self):
        form_data = {'name': 'name', 'address': 'address', 'max_capacity': 10, 'NIF': '1234567x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_NIF_9_numbers(self):
        form_data = {'name': 'name', 'address': 'address', 'max_capacity': 10, 'NIF': '123456789x'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_NIF_no_letter(self):
        form_data = {'name': 'name', 'address': 'address', 'max_capacity': 10, 'NIF': '12345678'}
        form = ClubModelForm(data=form_data)
        self.assertFalse(form.is_valid())
