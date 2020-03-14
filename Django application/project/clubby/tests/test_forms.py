import datetime

from django.test import TestCase
from django.utils import timezone

from clubby.forms.forms import SignupForm



# these tests are part of the following tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

#######################
#    CLUBBY TESTS     #
#######################

#This type of tests are unit tests but you can also test views:
#This is an example test
class YourTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)


class SignUpFormTest(TestCase):
    def test_sign_up_form_first_name_char_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'first_name')

    def test_sign_up_form_first_name_char_field_help_text(self):
        form = SignupForm()
        self.assertTrue(form.fields['first_name'].help_text, 'Required. 30 character max')

