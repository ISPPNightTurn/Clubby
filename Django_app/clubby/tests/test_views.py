import datetime

import unittest
from django.test import Client
from django.utils import timezone
from django.urls import reverse
import json


# these tests are part of the following tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

#######################
#    CLUBBY TESTS     #
#######################

# This type of tests are unit tests but you can also test views:
# This is an example test

class TestGETViews(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    # Test #1: This is a test for the view of the home page of clubby
    def test_view_url_clubby_home(self):
        response = self.client.get('/clubby/')

        self.assertEqual(response.status_code, 200)

    # Test #2: This is a test for the view of the events registered in clubby
    def test_view_url_clubby_events_GET(self):
        response = self.client.get('/clubby/events')

        self.assertEqual(response.status_code, 200)

    # Test #3: This is a test for the view of the clubs registered in clubby
    def test_view_url_clubby_clubs_GET(self):
        response = self.client.get('/clubby/clubs')

        self.assertEqual(response.status_code, 200)

    # Test #4: This is a test for the view of the login page of clubby
    def test_view_url_clubby_login_GET(self):
        response = self.client.get('/clubby/accounts/login/?next=/clubby/')

        self.assertEqual(response.status_code, 200)

    # Test #5: This is a test for the view of the sign up page of clubby
    def test_view_url_clubby_sign_up_GET(self):
        response = self.client.get('/clubby/signup/user')

        self.assertEqual(response.status_code, 200)

    # Test #6: This is a test for the view of the password reset page of clubby
    def test_view_url_clubby_password_reset_GET(self):
        response = self.client.get('/clubby/accounts/password_reset')

        self.assertEqual(response.status_code, 301)

    # Test #7: This is a test for the view of the profile page of clubby
    def test_view_url_clubby_profile_GET(self):
        response = self.client.get('/clubby/profile')

        self.assertEqual(response.status_code, 302)

    # #Test #8: This is a test for the view for adding funds
    # def test_view_url_clubby_adding_funds_GET(self):
    #     response = self.client.get('/clubby/addFunds?next=/clubby/profile')

    #     self.assertEqual(response.status_code, 302)

    # Test #9: This is a test for the view for viewing your events
    def test_view_url_clubby_my_events_GET(self):
        response = self.client.get('/clubby/myevents')

        self.assertEqual(response.status_code, 302)

    # Test #10: This is a test for the view for creating a event
    def test_view_url_clubby_create_event_GET(self):
        response = self.client.get('/clubby/event/create')

        self.assertEqual(response.status_code, 302)

    # Test #11: This is a test for the view for viewing your purchases
    def test_view_url_clubby_purchase_list_GET(self):
        response = self.client.get('/clubby/purchase/list/')

        self.assertEqual(response.status_code, 302)

    # Test #12: This is a test for the view for viewing your history
    def test_view_url_clubby_history_list_GET(self):
        response = self.client.get('/clubby/history/list/')

        self.assertEqual(response.status_code, 302)

    # Test #13: This is a test for the view for creating a club
    def test_view_url_clubby_create_club_GET(self):
        response = self.client.get('/clubby/club/create/')

        self.assertEqual(response.status_code, 302)

    # Test #14: This is a test for the view for creating a product
    def test_view_url_clubby_create_product_GET(self):
        response = self.client.get('/clubby/product/create/')

        self.assertEqual(response.status_code, 302)

   # Test #15: This is a test for the view for testing a wrong view
    def test_view_url_clubby_create_something_wrong_GET(self):
        response = self.client.get('/clubby/wrong/')

        self.assertEqual(response.status_code, 404)
