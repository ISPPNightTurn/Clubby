import datetime

from django.test import TestCase
from django.utils import timezone

from clubby.forms import ClubModelForm, SignupForm, ProductModelForm, EventModelForm, TicketCreateModelForm, RatingCreateModelForm

from datetime import datetime, timedelta

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

class SignupFormTests(TestCase):
    def test_form_complete(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_user_null(self):
        form_data = {'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_first_name_null(self):
        form_data = {'username': 'username', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_first_name_too_long(self):
        form_data = {'username': 'username', 'first_name': 'fnamefnamefnamefnamefnamefnamefname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_last_name_null(self):
        form_data = {'username': 'username', 'first_name': 'fname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_last_name_too_long(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lnamelnamelnamelnamelnamelnamelname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_email_null(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_email_not_email(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_email_too_long(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_bio_null(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_bio_too_long(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname', 'bio' : 'toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo long',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_birth_day_out_of_range(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 111, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_birth_year_out_of_range(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': -1, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_birth_month_out_of_range(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 22, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_location_null(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_location_too_long(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio','location': 'locationlocationlocationlocationlocation', 'password1': 'contrasenia', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_password1_null(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_password2_null(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_passwords_not_same(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'contras', 'password2': 'contrasenia'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_passwords_empty(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': '', 'password2': ''}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_passwords_easy(self):
        form_data = {'username': 'username', 'first_name': 'fname', 'last_name': 'lname',
        'email': 'a@gamil.com', 'birth_day': 1, 'birth_year': 1997, 'birth_month': 1, 
        'bio': 'bio', 'location': 'location', 'password1': 'pass', 'password2': 'pass'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

class ProductModelFormTests(TestCase):
    def test_form_complete(self):
        form_data = {'name': 'name', 'price': 1, 'product_type': 'm', 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_name_null(self):
        form_data = {'price': 1, 'product_type': 'm', 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_name_too_long(self):
        form_data = {'name': 'namenamenamenamenamenamenamenamenamenamenamenamename', 'price': 1, 'product_type': 'm', 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_price_null(self):
        form_data = {'name': 'name', 'product_type': 'm', 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Por implementar
    # def test_form_price_neg(self):
    #     form_data = {'name': 'name', 'price': -1, 'product_type': 'm', 'reservation_exclusive': False}
    #     form = ProductModelForm(data=form_data)
    #     self.assertFalse(form.is_valid())

    def test_form_product_type_null(self):
        form_data = {'name': 'name', 'price': 1, 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_product_type_other_value(self):
        form_data = {'name': 'name', 'product_type': 'x', 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_product_type_long(self):
        form_data = {'name': 'name', 'product_type': 'xxx', 'reservation_exclusive': False}
        form = ProductModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Si no se añade es como false
    def test_form_reservation_exclusive_null(self):
        form_data = {'name': 'name', 'price': 1, 'product_type': 'm'}
        form = ProductModelForm(data=form_data)
        self.assertTrue(form.is_valid())

class EventModelFormTests(TestCase):
    def test_form_complete(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'duration': 10, 'picture': 'https://picture.com', 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_picture_null(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'duration': 10, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_name_null(self):
        form_data = {'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'duration': 10, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_name_too_long(self):
        form_data = {'name': 'name toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo long', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'duration': 10, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_start_time_null(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'duration': 10, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_start_time_neg(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': -1, 'duration': 10, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_duration_null(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_duration_neg(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'duration': -1, 'event_type': 'c'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_event_type_null(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'duration': 10}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_event_other_value(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'duration': 10, 'event_type': 'x'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_event_type_long(self):
        form_data = {'name': 'name', 'start_date': datetime.strptime("2020/04/04", "%Y/%m/%d"),
        'start_time': 10, 'duration': 10, 'event_type': 'ccc'}
        form = EventModelForm(data=form_data)
        self.assertFalse(form.is_valid())
