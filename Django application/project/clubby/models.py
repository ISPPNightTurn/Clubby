from django.db import models
import datetime
from datetime import timezone
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

    class Meta:
        permissions = (("can_add_event", "Set event to be had."),)
    
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
    class Meta:
        permissions = (("can_mark_assistance", "Set event to assist."),) 

    name = models.CharField(max_length=200,)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    start_date = models.DateTimeField()

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
    
    atendees = models.ManyToManyField(User)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this event."""
        return reverse('event-detail', args=[str(self.id)])

class Ticket(models.Model):

    price = models.DecimalField(decimal_places=2)
    date = models.DateTimeField()
    ticket_id = models.CharField

    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    owner =  models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    

class Reservation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField
    price = models.DecimalField(decimal_places=2)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

class Hookah(models.Model):
    price = models.DecimalField(decimal_places=2)
    flavour = models.CharField(max_length=50)  
    club = models.ForeignKey(Club,on_delete=models.CASCADE)

class Rating(models.Model):
    text = models.CharField(max_length=500)
    stars = models.IntegerField(min=0,max=10)
    recommended = models.BooleanField()
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADES)

class Receipt(models.Model):
    date = models.DateTimeField()
    amount = models.IntegerField(default=0)
    #Every kind of product is optional
    #Amount parameter refers to amount of product x
    #We take for granted that the user will only order a reservation or a hookah everytime
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    hookah = models.ForeignKey(Hookah,on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)


   
