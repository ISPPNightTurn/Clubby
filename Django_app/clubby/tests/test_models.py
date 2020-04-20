import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import Profile, User, Club, Event, Ticket, CreateTicket, Product, Rating, QR_Item

from datetime import datetime, timedelta



# these tests are part of the following tutorial:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
#it contains a lot of information about them so you dhould check it out if you have been assigned testing...
# there is some info about coverage and selenium they are surely gonna ask us about so read upon it.

#######################
#    CLUBBY TESTS     #
#######################

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.user.save()
        self.test_profile = Profile(user = self.user, bio = "Bio", location = "Sevilla",
            birth_date = datetime.strptime("1997/01/01", "%Y/%m/%d"), funds = 10, picture = "https://picture.com",
            renew_premium = True)

    def test_profile_to_user(self):
        self.assertEquals(self.test_profile.user, self.user)

    def test_profile_to_string_bio(self):
        self.assertEquals(str(self.test_profile.bio), "Bio")

    def test_profile_to_string_location(self):
        self.assertEquals(str(self.test_profile.location), "Sevilla")

    def test_profile_to_string_birth_date(self):
        self.assertEquals(str(self.test_profile.birth_date), "1997-01-01 00:00:00")

    def test_profile_to_funds(self):
        self.assertEquals(self.test_profile.funds, 10)

    def test_profile_to_string_picture(self):
        self.assertEquals(str(self.test_profile.picture), "https://picture.com")

    def test_profile_to_renew_premium(self):
        self.assertEquals(self.test_profile.renew_premium, True)

    def tearDown(self):
        self.user.delete()

class ClubModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.user.save()
        self.test_club = Club(name = "Clubby", address = "Callesita", max_capacity = 120, NIF = '12345678X',
            picture = "https://picture.com", owner = self.user)

    def test_club_to_string_name(self):
        self.assertEquals(str(self.test_club.name), "Clubby")

    def test_club_to_string_address(self):
        self.assertEquals(str(self.test_club.address), "Callesita")

    def test_club_to_max_capacity(self):
        self.assertEquals(self.test_club.max_capacity, 120)

    def test_club_to_string_NIF(self):
        self.assertEquals(str(self.test_club.NIF), '12345678X')

    def test_club_to_string_picture(self):
        self.assertEquals(str(self.test_club.picture), "https://picture.com")

    def test_club_to_owner(self):
        self.assertEquals(self.test_club.owner, self.user)

    def tearDown(self):
        self.user.delete()


class EventModelTest(TestCase):

    def setUp(self):
        self.club = Club()
        self.user = User()
        self.user.save()
        self.test_event = Event(name = "Evento", club = self.club, start_date = datetime.strptime("2021/01/01", "%Y/%m/%d"),
            start_time = 12, duration = 4, picture = "https://picture.com", event_type = 'c')

    def test_event_to_string_name(self):
        self.assertEquals(str(self.test_event.name), "Evento")

    def test_event_to_club(self):
        self.assertEquals(self.test_event.club, self.club)

    def test_event_to_string_start_date(self):
        self.assertEquals(str(self.test_event.start_date), "2021-01-01 00:00:00")

    def test_event_to_start_time(self):
        self.assertEquals(self.test_event.start_time, 12)

    def test_event_to_duration(self):
        self.assertEquals(self.test_event.duration, 4)

    def test_event_to_string_picture(self):
        self.assertEquals(str(self.test_event.picture), "https://picture.com")

    def test_event_to_string_event_type(self):
        self.assertEquals(str(self.test_event.event_type), 'c')        

    def tearDown(self):
        self.user.delete()

class TicketModelTest(TestCase):

    def setUp(self):
        self.club = Club()
        self.event = Event(name = "Evento", club = self.club, start_date = datetime.strptime("2021/01/01", "%Y/%m/%d"),
            start_time = 12, duration = 4, picture = "https://picture.com")
        self.user = User()
        self.user.save()

        self.test_ticket = Ticket(price = 5.5, category = "Basic", description = "Descrition",
            event = self.event, user = self.user)

    def test_ticket_to_price(self):
        self.assertEquals(self.test_ticket.price, 5.5)

    def test_ticket_to_string_category(self):
        self.assertEquals(str(self.test_ticket.category), "Basic")

    def test_ticket_to_string_description(self):
        self.assertEquals(str(self.test_ticket.description), "Descrition")

    def test_ticket_to_event(self):
        self.assertEquals(self.test_ticket.event, self.event)

    def test_ticket_to_user(self):
        self.assertEquals(self.test_ticket.user, self.user)

    def tearDown(self):
        self.user.delete()

class CreateTicketModelTest(TestCase):

    def setUp(self):
        self.club = Club()
        self.event = Event(name = "Evento", club = self.club, start_date = datetime.strptime("2021/01/01", "%Y/%m/%d"),
            start_time = 12, duration = 4, picture = "https://picture.com")
        self.user = User()
        self.user.save()

        self.test_create_ticket = CreateTicket(price = 5.5, category = "Basic", description = "Descrition",
            size = 100, event = self.event, user = self.user)

    def test_create_ticket_to_price(self):
        self.assertEquals(self.test_create_ticket.price, 5.5)

    def test_create_ticket_to_string_category(self):
        self.assertEquals(str(self.test_create_ticket.category), "Basic")

    def test_create_ticket_to_string_description(self):
        self.assertEquals(str(self.test_create_ticket.description), "Descrition")

    def test_create_ticket_to_size(self):
        self.assertEquals(self.test_create_ticket.size, 100)

    def test_create_ticket_to_event(self):
        self.assertEquals(self.test_create_ticket.event, self.event)

    def test_create_ticket_to_user(self):
        self.assertEquals(self.test_create_ticket.user, self.user)

    def tearDown(self):
        self.user.delete()

class ProductModelTest(TestCase):

    def setUp(self):
        self.club = Club()

        self.test_product = Product(name = "Cerveza", price = 1.5, club = self.club, product_type = 'm',
            reservation_exclusive = False)

    def test_product_to_string_name(self):
        self.assertEquals(str(self.test_product.name), "Cerveza")
        
    def test_product_to_price(self):
        self.assertEquals(self.test_product.price, 1.5)

    def test_product_to_club(self):
        self.assertEquals(self.test_product.club, self.club)

    def test_product_to_string_product_type(self):
        self.assertEquals(str(self.test_product.product_type), 'm')

    def test_product_to_reservation_exclusive(self):
        self.assertEquals(self.test_product.reservation_exclusive, False)

# class ReservationModelTest(TestCase):

#     def setUp(self):
#         self.club = Club()
#         self.event = Event(name = "Evento", club = self.club, start_date = datetime.strptime("2021/01/01", "%Y/%m/%d"),
#             start_time = 12, duration = 4, picture = "https://picture.com")

#         self.test_reservation = Reservation(max_time = 12, price = 40,event = self.event)

#     def test_reservation_to_max_time(self):
#         self.assertEquals(self.test_reservation.max_time, 12)

#     def test_reservation_to_price(self):
#         self.assertEquals(self.test_reservation.price, 40)

#     def test_reservation_to_event(self):
#         self.assertEquals(self.test_reservation.event, self.event)

class RatingModelTest(TestCase):

    def setUp(self):
        self.club = Club()
        self.user = User()
        self.user.save()
    
        self.test_rating = Rating(text = "TEXTO AQUI", stars = 10, fecha = datetime.strptime("2021/01/01", "%Y/%m/%d"),
            club = self.club, user = self.user)

    def test_rating_to_text(self):
        self.assertEquals(str(self.test_rating.text), "TEXTO AQUI")

    def test_rating_to_stars(self):
        self.assertEquals(self.test_rating.stars, 10)

    def test_rating_to_string_fecha(self):
        self.assertEquals(str(self.test_rating.fecha), "2021-01-01 00:00:00")

    def test_rating_to_club(self):
        self.assertEquals(self.test_rating.club, self.club)

    def test_rating_to_user(self):
        self.assertEquals(self.test_rating.user, self.user)

    def tearDown(self):
        self.user.delete()

class QR_ItemModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.user.save()
        self.club = Club()
        self.product = Product(name = "Cerveza", price = 1.5, club = self.club, product_type = 'm',
            reservation_exclusive = False)
    
        self.test_qr_item = QR_Item(is_used = False, product = self.product, ticket = None,
            user = self.user, fecha = datetime.strptime("2021/01/01", "%Y/%m/%d"), priv_key = '12345')

    def test_qr_item_to_is_used(self):
        self.assertEquals(self.test_qr_item.is_used, False)

    def test_qr_item_to_product(self):
        self.assertEquals(self.test_qr_item.product, self.product)

    def test_qr_item_to_ticket(self):
        self.assertEquals(self.test_qr_item.ticket, None)

    def test_qr_item_to_user(self):
        self.assertEquals(self.test_qr_item.user, self.user)

    def test_qr_item_to_string_fecha(self):
        self.assertEquals(str(self.test_qr_item.fecha), "2021-01-01 00:00:00")

    def test_qr_item_to_string_priv_key(self):
        self.assertEquals(str(self.test_qr_item.priv_key), "12345")

    def tearDown(self):
        self.user.delete()
