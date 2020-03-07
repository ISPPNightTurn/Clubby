from django.db import models
import datetime
from datetime import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# This is the models file, here we create the django objects we need for our application to work
# these first two models are here as testing grounds and should be deleted later on.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    # this is a reference to the Question class as a many to one configuration
    # if you are using VSCode you can see that by hovering on ForeignKey
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

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
    price = models.IntegerField(default = 0, help_text= 'The ticket price for your event, 0 if free.')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this event."""
        return reverse('event-detail', args=[str(self.id)])