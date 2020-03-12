from django.db import models
import datetime
from datetime import timezone, timedelta
from django.contrib.auth.models import User
from django.urls import reverse


####################
#      CLUBBY      #
####################

# We will be extending the default user model of django instead of creating a new model ourselves.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)+' profile'
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this user."""
        return reverse('user-detail', args=[str(self.user.id)])

    class Meta:
        permissions = (("is_user", "Is a user and can do everything an identified user can."),
        ("is_owner", "Is an owner and can do everything an identified owner can."),
        ("is_premium_owner", "Is a premium owner and can do everything an identified owner can and more.")) 
    
    #this is a property it can return multiple stuff and can be called from a template.
    @property
    def is_premium(self):
        for g in self.user__groups: # this might be user.groups idk.
            if("premium" in str(g)):
                return True
        return False

# The order in django models matters, we cannot create the Event model without defining the Club model first
class Club(models.Model):
    '''
    Model representing the clubs that the owners will register.
    '''
    name = models.CharField(max_length=50, help_text='Enter the name of your club.')
    address = models.CharField(max_length=200, help_text='Enter the full address so google maps can find it.')
    max_capacity = models.IntegerField(help_text = 'The capacity of your club, you\'re responsible for the enforcement of this number.')
    NIF = models.CharField(max_length=10, help_text = 'Company number for the club')
    
    # This represents the owners user.
    owner = models.OneToOneField(User, on_delete=models.CASCADE)        
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this club."""
        return reverse('club-detail', args=[str(self.id)])

#for the get_absolute_url method to work we need to define some shit for it to work.

    
class Event(models.Model):
    '''
    Model representing the events that will happen on a club
    '''
    name = models.CharField(max_length=200,)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.IntegerField(max_length=2,help_text='event start time 24h format.', default=12)
    duration = models.IntegerField(max_length=2,help_text='event duration in hours, max is 12 hours',default=12)
    atendees = models.ManyToManyField(User)

    EVENT_TYPE = (
        ('c', 'casual'),
        ('f', 'fancy'),
        ('d', 'dress_up'),
        ('p', 'private'),
    )
    event_type = models.CharField(
        max_length=1,
        choices=EVENT_TYPE,
        blank=True,
        default='c',
        help_text='event type',
    ) 
    @property
    def start_datetime(self):
        dur = datetime.timedelta(hours=self.start_time)
        return self.start_date + dur

    @property
    def end_date(self):
        dur = datetime.timedelta(hours=self.duration)
        return self.start_datetime + dur

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this event."""
        return reverse('event-detail', args=[str(self.id)])

class Ticket(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=5)#999,99 es el maximo
    date = models.DateTimeField()
    # ticket_id = models.CharField()#<-- podemos usar a primary key para identificarlos, este tributo es redundante.

    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=5)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this product."""
        return reverse('product-detail', args=[str(self.id)])
    

class Reservation(models.Model):
    max_time = models.IntegerField(help_text="max hours after the event starts people can arrive at.", max_length=2, default=4)
    price = models.DecimalField(decimal_places=2,max_digits=5)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + ' ' + str(self.price) + ' ' + str(self.max_time)


class Rating(models.Model):
    text = models.TextField(max_length=500)
    stars = models.IntegerField(help_text='star rating 1-10')
    recommended = models.BooleanField(help_text='would you recommend this club?')
    club = models.ForeignKey(Club, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.club)+' '+str(self.stars)

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField()

    def __str__(self):
        to_print = ""
        to_print += str(self.user) + "[ "
        for x in self.products:
            to_print += str(x+", ")
        to_print += "]"
        return to_print


class Order(models.Model):
    date = models.DateTimeField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    basket = models.ManyToManyField(Basket)

    def __str__(self):
        return str(self.pk) +' '+str(self.user) +' '+str(self.date)

class QR_Item(models.Model):
    is_used = models.BooleanField(default=False)
    #The order is used so we can find the user and give them all his QR items
    #A QR_Item can be either a product, a reservation or a ticket
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    reservation = models.OneToOneField(Reservation,on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    private_key = models.CharField(max_length=128)

    def __str__(self):
        return str(self.private_key)

