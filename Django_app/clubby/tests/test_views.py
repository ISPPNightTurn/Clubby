
import unittest
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
import json
from django.test.client import Client

from ..models import Profile, User, Club, Event, Ticket, CreateTicket, Product, Rating, QR_Item
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# these tests are part of the following tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

#######################
#    CLUBBY TESTS     #
#######################

class ClubbyViewsTestingOkResponses(TestCase):
    def setUp(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('pruebaviews', 'myemail@test.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)

        self.user = User()
        self.user.save()
        self.test_profile = Profile(user = self.user, bio = "Bio", location = "Sevilla",
            birth_date = datetime.strptime("1997/01/01", "%Y/%m/%d"), funds = 10, picture = "https://picture.com",
            renew_premium = True)

    def test_profile_to_user(self):
        self.assertEquals(self.test_profile.user, self.user)
    
    #Test #1: This is a test for the view of the home page of clubby
    def test_view_url_clubby_home(self): 
        response = self.client.get('/clubby/') 
        self.assertEquals(response.status_code, 200)

    #Test #2: This is a test for the view of the events registered in clubby
    def test_view_url_clubby_events_GET(self): 
        response = self.client.get('/clubby/events') 
        self.assertEqual(response.status_code, 200)

    #Test #3: This is a test for the view of the clubs registered in clubby
    def test_view_url_clubby_clubs_GET(self): 
        response = self.client.get('/clubby/clubs') 
        self.assertEqual(response.status_code, 301)  

    #Test #4: This is a test for the view of the login page of clubby
    def test_view_url_clubby_login_GET(self): 
        response = self.client.get('/clubby/accounts/login/?next=/clubby/') 
        self.assertEqual(response.status_code, 200)

    #Test #5: This is a test for the view of the sign up page of clubby
    def test_view_url_clubby_sign_up_GET(self): 
        response = self.client.get('/clubby/signup/user') 
        self.assertEqual(response.status_code, 200)
    
    #Test #6: This is a test for the view of the sign up page for an owner of clubby
    def test_view_url_clubby_sign_up_owner_GET(self): 
        response = self.client.get('/clubby/signup/owner') 
        self.assertEqual(response.status_code, 200)

    #Test #7: This is a test for the view of terms and conditions
    def test_view_url_clubby_terms_owner_GET(self): 
        response = self.client.get('/clubby/terms-and-conditions') 
        self.assertEqual(response.status_code, 200)

    #Test #8: This is a test for the view of the rating list of a created club
    def test_view_url_clubby_created_club_rating_list_GET(self): 
        response = self.client.get('/clubby/club/1/rating_list') 
        self.assertEqual(response.status_code, 200)  

 #Test #9: This is a test for the view of the rating create view of a created club
    def test_view_url_clubby_created_club_rating_create_GET(self): 
        response = self.client.get('/clubby/club/1/rating_create') 
        self.assertEqual(response.status_code, 200)        

class ClubbyViewsTestingMovedPermanentlyResponses(TestCase):
    def setUp(self):
        self.client_anonymous = Client()
        self.user = User()

    #Test #1: This is a test for the view of the password reset page of clubby
    def test_view_url_clubby_password_reset_GET(self): 
        response = self.client.get('/clubby/accounts/password_reset') 
        self.assertEqual(response.status_code, 301) 

class ClubbyViewsTestingNotFoundResponses(TestCase):
    def setUp(self):
        self.client_anonymous = Client()
        self.user = User()

   #Test #1: This is a test for the view for testing a wrong view
    def test_view_url_clubby_create_something_wrong_GET(self): 
        response = self.client.get('/clubby/wrong/') 
        self.assertEqual(response.status_code, 404)  

class ClubbyViewsTestingFoundResponses(TestCase):
    def setUp(self):
        self.client_anonymous = Client()
        self.user = User()

    #Test #1: This is a test for the view of the profile page of clubby
    def test_view_url_clubby_profile_GET(self): 
        response = self.client.get('/clubby/profile') 
        self.assertEqual(response.status_code, 302)

    #Test #2: This is a test for the view for adding funds
    def test_view_url_clubby_adding_funds_GET(self): 
        response = self.client.get('/clubby/addFunds/31') 
        self.assertEqual(response.status_code, 302)

    #Test #3: This is a test for the view for viewing your events
    def test_view_url_clubby_my_events_GET(self): 
        response = self.client.get('/clubby/myevents') 
        self.assertEqual(response.status_code, 302)

    #Test #4: This is a test for the view for creating a event
    def test_view_url_clubby_create_event_GET(self): 
        response = self.client.get('/clubby/event/create') 
        self.assertEqual(response.status_code, 302)

    #Test #5: This is a test for the view for viewing your purchases
    def test_view_url_clubby_purchase_list_GET(self): 
        response = self.client.get('/clubby/purchase/list/') 
        self.assertEqual(response.status_code, 302)

    #Test #6: This is a test for the view for viewing your history
    def test_view_url_clubby_history_list_GET(self): 
        response = self.client.get('/clubby/history/list/') 
        self.assertEqual(response.status_code, 302)

    #Test #7: This is a test for the view for creating a club
    def test_view_url_clubby_create_club_GET(self): 
        response = self.client.get('/clubby/club/create/') 
        self.assertEqual(response.status_code, 302)

    #Test #8: This is a test for the view for creating a product
    def test_view_url_clubby_create_product_GET(self): 
        response = self.client.get('/clubby/product/create/') 
        self.assertEqual(response.status_code, 302) 

   #Test #7: This is a test for the view for google login
    def test_view_url_clubby_login_google_GET(self): 
        response = self.client.get('/clubby/login/google-oauth2/') 
        self.assertEqual(response.status_code, 302)
   
    #Test #8: This is a test for the view of edit profile
    def test_view_url_clubby_profile_edit_GET(self): 
        response = self.client.get('/clubby/profile/edit') 
        self.assertEqual(response.status_code, 302)

    #Test #9: This is a test for the view of added fund
    def test_view_url_clubby_added_fund_GET(self): 
        response = self.client.get('/clubby/charge/22200') 
        self.assertEqual(response.status_code, 302)        
