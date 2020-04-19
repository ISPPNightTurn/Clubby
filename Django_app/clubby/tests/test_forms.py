import datetime

from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from clubby.forms import ClubModelForm, SignupForm, ProductModelForm, EventModelForm, TicketCreateModelForm, RatingCreateModelForm, ProductPurchaseForm, RedeemQRCodeForm, TicketPurchaseForm, FundsForm, PremiumForm, SearchForm, SearchEventForm
from ..models import Club, Product, User, QR_Item
from django.contrib.auth.models import User

from datetime import datetime, timedelta

#######################
#    CLUBBY TESTS     #
#######################

import datetime

from django.test import TestCase
from django.utils import timezone

from clubby.forms import ClubModelForm, SignupForm, ProductModelForm, EventModelForm, TicketCreateModelForm, RatingCreateModelForm

from datetime import datetime, timedelta

#######################
#    CLUBBY TESTS     #
#######################

#################################### JAVI ####################################
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

class TicketCreateModelFormTests(TestCase):
    def test_form_complete(self):
        form_data = {'price': 10, 'category': 'category', 'description': 'description', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertTrue(form.is_valid())

    def test_form_price_null(self):
        form_data = {'category': 'category', 'description': 'description', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_price_too_big(self):
        form_data = {'price': 1000, 'category': 'category', 'description': 'description', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())
    
    def test_form_category_null(self):
        form_data = {'price': 10, 'description': 'description', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_category_too_long(self):
        form_data = {'price': 10, 'category': 'categorycategorycategorycategorycategorycategory', 'description': 'description', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_description_null(self):
        form_data = {'price': 10, 'category': 'category', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_description_too_long(self):
        form_data = {'price': 10, 'category': 'category', 'description': 'descriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescription', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_size_null(self):
        form_data = {'price': 10, 'category': 'category', 'description': 'description'}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())
    
    def test_form_size_bigger_max(self):
        form_data = {'price': 10, 'category': 'category', 'description': 'description', 'size': 110}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_size_neg(self):
        form_data = {'price': 10, 'category': 'category', 'description': 'description', 'size': -1}
        form = TicketCreateModelForm(data=form_data, max=100)
        self.assertFalse(form.is_valid())

    def test_form_max_null(self):
        form_data = {'price': 10, 'category': 'category', 'description': 'description', 'size': 100}
        form = TicketCreateModelForm(data=form_data, max=None)
        self.assertTrue(form.is_valid())

class RatingCreateModelFormTests(TestCase):
    def test_form_complete(self):
        form_data = {'stars': 10, 'text': 'text'}
        form = RatingCreateModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_stars_null(self):
        form_data = {'text': 'text'}
        form = RatingCreateModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_stars_neg(self):
        form_data = {'stars': -1, 'text': 'text'}
        form = RatingCreateModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_stars_too_big(self):
        form_data = {'stars': 11, 'text': 'text'}
        form = RatingCreateModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_text_null(self):
        form_data = {'stars': 10}
        form = RatingCreateModelForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_text_too_long(self):
        form_data = {'stars': 10, 'text': 'toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo long'}
        form = RatingCreateModelForm(data=form_data)
        self.assertFalse(form.is_valid())

#################################### YASSIN ####################################
class ProductPurchaseFormTest(TestCase):
    #Test 1 - Yassin
    def test_form_complete(self):
        self.user = User()
        self.user.save()
        club = Club.objects.create(name = "Clubby", address = "Callesita", max_capacity = 120, NIF = '12345678X',
            picture = "https://picture.com", owner = self.user)
        product = Product.objects.create(name = "Cerveza", price = 1.5, club = club, product_type = 'm',
            reservation_exclusive = False)            
        form_data = {'quantity': 2, 'product': product.id}
        form = ProductPurchaseForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Test 2 - Yassin
    def test_form_quantity_too_big(self):
        self.user = User()
        self.user.save()
        club = Club.objects.create(name = "Clubby", address = "Callesita", max_capacity = 120, NIF = '12345678X',
            picture = "https://picture.com", owner = self.user)
        product = Product.objects.create(name = "Cerveza", price = 1.5, club = club, product_type = 'm',
            reservation_exclusive = False)        
        form_data = {'quantity': 12, 'product': product.id}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 3 - Yassin
    def test_form_quantity_too_small(self):
        self.user = User()
        self.user.save()
        club = Club.objects.create(name = "Clubby", address = "Callesita", max_capacity = 120, NIF = '12345678X',
            picture = "https://picture.com", owner = self.user)
        product = Product.objects.create(name = "Cerveza", price = 1.5, club = club, product_type = 'm',
            reservation_exclusive = False)
        form_data = {'quantity': 0, 'product': product.id}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 4 - Yassin
    def test_form_quantity_negative(self):
        self.user = User()
        self.user.save()
        club = Club.objects.create(name = "Clubby", address = "Callesita", max_capacity = 120, NIF = '12345678X',
            picture = "https://picture.com", owner = self.user)
        product = Product.objects.create(name = "Cerveza", price = 1.5, club = club, product_type = 'm',
            reservation_exclusive = False)
        form_data = {'quantity': -1, 'product': product.id}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 5 - Yassin
    def test_form_quantity_null(self):
        self.user = User()
        self.user.save()
        club = Club.objects.create(name = "Clubby", address = "Callesita", max_capacity = 120, NIF = '12345678X',
            picture = "https://picture.com", owner = self.user)
        product = Product.objects.create(name = "Cerveza", price = 1.5, club = club, product_type = 'm',
            reservation_exclusive = False) 
        form_data = {'product': product.id}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 6 - Yassin
    def test_form_product_null(self):
        form_data = {'quantity': 1}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 7 - Yassin
    def test_form_quantity_wrong_type(self):
        form_data = {'quantity': 'string', 'product': 123}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 8 - Yassin
    def test_form_product_wrong_type(self):
        form_data = {'quantity': 1, 'product': 'string'}
        form = ProductPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 10 - Yassin
    def test_form_qr_item_null(self):
        form_data = {}
        form = RedeemQRCodeForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 11 - Yassin
    def test_form_qr_item_wrong_type(self):
        form_data = {'qr_item_id': 'string'}
        form = RedeemQRCodeForm(data=form_data)
        self.assertFalse(form.is_valid())
    
class TicketPurchaseFormTest(TestCase):
    #Test 12 - Yassin
    def test_form_complete(self):    
        form_data = {'quantity': 4, 'event': 1, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Test 13 - Yassin
    def test_form_quantity_too_big(self):
        form_data = {'quantity': 5, 'event': 1, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 14 - Yassin
    def test_form_quantity_too_small(self):
        form_data = {'quantity': 0, 'event': 1, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 15 - Yassin
    def test_form_quantity_negative(self):
        form_data = {'quantity': -2, 'event': 1, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 16 - Yassin
    def test_form_quantity_null(self):
        form_data = {'event': 1, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 17 - Yassin
    def test_form_event_null(self):
        form_data = {'quantity': 2, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 18 - Yassin
    def test_form_category_too_long(self):
        form_data = {'event': 1, 'quantity': 2, 'category': 'toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolong'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 19 - Yassin
    def test_form_category_null(self):
        form_data = {'quantity': 2, 'event': 1}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 20 - Yassin
    def test_form_quantity_wrong_type(self):
        form_data = {'quantity': 'string', 'event': 1, 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 21 - Yassin
    def test_form_event_wrong_type(self):
        form_data = {'quantity': 2, 'event': 'string', 'category': 'string'}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    #Test 22 - Yassin
    def test_form_category_wrong_type(self):
        form_data = {'quantity': 2, 'event': 'string', 'category': 2}
        form = TicketPurchaseForm(data=form_data)
        self.assertFalse(form.is_valid())

class FundsFormTest(TestCase):
    #Test 23 - Yassin
    def test_form_complete(self):    
        form_data = {'ammount': 101}
        form = FundsForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Test 24 - Yassin
    def test_form_amount_too_big(self):
        form_data = {'ammount': 505}
        form = FundsForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 25 - Yassin
    def test_form_amount_too_small(self):
        form_data = {'ammount': 5}
        form = FundsForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 26 - Yassin
    def test_form_amount_negative(self):
        form_data = {'ammount': -50}
        form = FundsForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 27 - Yassin
    def test_form_amount_null(self):
        form_data = {}
        form = FundsForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    #Test 28 - Yassin
    def test_form_amount_wrong_type(self):
        form_data = {'ammount': 'string'}
        form = FundsForm(data=form_data)
        self.assertFalse(form.is_valid())

class PremiumFormTest(TestCase):
    #Test 29 - Yassin
    def test_form_complete_true_case(self):    
        form_data = {'accept': True}
        form = PremiumForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Test 30 - Yassin
    def test_form_complete_false_case(self):    
        form_data = {'accept': False}
        form = PremiumForm(data=form_data)
        self.assertFalse(form.is_valid())

    #Test 31 - Yassin
    def test_form_null_accept(self):    
        form_data = {}
        form = PremiumForm(data=form_data)
        self.assertFalse(form.is_valid())

class SearchEventFormTest(TestCase):
    #Test 32 - Yassin
    def test_form_complete(self):    
        form_data = {'start_date': datetime.strptime("2021/01/04", "%Y/%m/%d"), 'end_date': datetime.strptime("2021/01/06", "%Y/%m/%d")}
        form = SearchEventForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Test 33 - Yassin
    def test_form_start_date_after_end_date(self):    
        form_data = {'start_date': datetime.strptime("2021/01/04", "%Y/%m/%d"), 'end_date': datetime.strptime("2021/01/02", "%Y/%m/%d")}
        form = SearchEventForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    #Test 34 - Yassin
    def test_form_start_date_in_the_past(self):    
        form_data = {'start_date': datetime.strptime("2001/01/04", "%Y/%m/%d"), 'end_date': datetime.strptime("2021/01/02", "%Y/%m/%d")}
        form = SearchEventForm(data=form_data)
        self.assertFalse(form.is_valid())

class SearchFormTest(TestCase):
    #Test 35 - Yassin
    def test_form_complete(self):    
        form_data = {'query': 'string'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Test 36 - Yassin
    def test_form_null_query(self):    
        form_data = {}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        
