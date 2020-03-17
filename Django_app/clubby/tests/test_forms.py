import datetime

from django.test import TestCase
from django.utils import timezone

from clubby.forms import SignupForm
from clubby.forms import ProductModelForm
from clubby.forms import EventModelForm



# these tests are part of the following tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

#######################
#    CLUBBY TESTS     #
#######################

#This type of tests are unit tests but you can also test views:
#This is an example test
# class YourTestClass(TestCase):
#     def setUp(self):
#         # Setup run before every test method.
#         pass

#     def tearDown(self):
#         # Clean up run after every test method.
#         pass

#     def test_something_that_will_pass(self):
#         self.assertFalse(False)

#     def test_something_that_will_fail(self):
#         self.assertTrue(False)


class SignUpFormTest(TestCase):
    def test_sign_up_form_first_name_char_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'first_name')

    def test_sign_up_form_first_name_char_field_help_text(self):
        form = SignupForm()
        self.assertTrue(form.fields['first_name'].help_text, 'Required. 30 character max')


   
    def test_sign_up_form_email_email_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'email')

    def test_sign_up_form_email_email_field_help_text(self):
        form = SignupForm()
        self.assertTrue(form.fields['email'].help_text, 'Required. Inform a valid email address.')



    def test_sign_up_form_bith_date_date_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['birth_date'].label == None or form.fields['birth_date'].label == 'birth_date')

    def test_sign_up_form_birth_date_date_field_help_text(self):
        form = SignupForm()
        self.assertTrue(form.fields['birth_date'].help_text, 'Required, your birthday, format: YYYY-MM-DD')



    def test_sign_up_form_bio_char_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['bio'].label == None or form.fields['bio'].label == 'bio')

    def test_sign_up_form_bio_char_field_help_text(self):
        form = SignupForm()
        self.assertTrue(form.fields['bio'].help_text, 'Optional, tell us something about you.')




    def test_sign_up_form_location_char_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['location'].label == None or form.fields['location'].label == 'location')

    def test_sign_up_form_location_char_field_help_text(self):
        form = SignupForm()
        self.assertTrue(form.fields['bio'].help_text, 'Optional, where are you form?.')


    


class ProductModelFormTest(TestCase):

    def test_product_model_form_name_char_field_label(self):
        form = ProductModelForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['location'].label == 'location')

    def test_product_model_form_name_char_field_help_text(self):
        form = ProductModelForm()
        self.assertTrue(form.fields['name'].help_text, 'Required. 50 character max')




    def test_product_model_form_price_decimal_field_label(self):
        form = ProductModelForm()
        self.assertTrue(form.fields['price'].label == None or form.fields['price'].label == 'price')


    def test_product_model_form_price_decimal_field_help_text(self):
        form = ProductModelForm()
        self.assertTrue(form.fields['price'].help_text, 'Required. 5 digits max')




class EventModelFormTest(TestCase):

    def test_event_model_form_name_char_field_label(self):
        form = EventModelForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'name')

    def test_event_model_form_name_char_field_help_text(self):
        form = EventModelForm()
        self.assertTrue(form.fields['name'].help_text, 'Required. 50 character max')   



    def test_event_model_form_start_date_date_field_label(self):
        form = EventModelForm()
        self.assertTrue(form.fields['start_date'].label == None or form.fields['start_date'].label == 'price')


   