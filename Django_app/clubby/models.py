from django.db import models
import datetime
from datetime import timezone, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

####################
#      CLUBBY      #
####################
# this is used to set the path for image storing for the club and profile (which both have a 1 to 1 relationship with user class.)
def user_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/folder_name/<username>
    return 'profile_pics/{0}'.format(instance.user.username)

# We will be extending the default user model of django instead of creating a new model ourselves.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    funds = models.DecimalField(decimal_places=2, max_digits=5,default=0.0)
    picture = models.URLField(help_text='Post a picture of your pretty face, dude',null=True,blank=True)
    renew_premium = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)+' profile'


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
def owner_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/folder_name/<username>
    return 'club_pics/{0}'.format(instance.owner.username)

class Club(models.Model):
    '''
    Model representing the clubs that the owners will register.
    '''
    # picture = models.ImageField()
    name = models.CharField(max_length=50, help_text='Enter the name of your club.')
    address = models.CharField(max_length=200, help_text='Enter the full address so google maps can find it.')
    max_capacity = models.IntegerField(help_text = 'The capacity of your club, you\'re responsible for the enforcement of this number.')
    NIF = models.CharField(max_length=10, help_text = 'Company number for the club')
    picture = models.URLField(help_text = 'URL to a picture of your club',null=True,blank=True)
    # This represents the owners user.
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this club."""
        return reverse('club-detail', args=[str(self.id)])


def event_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/folder_name/<id>
    return 'event_pics/{0}'.format(instance.pk)

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
    picture = models.URLField(help_text="URL to the poster for the event",null=True,blank=True)
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
    def end_datetime(self):
        dur = datetime.timedelta(hours=self.duration)
        return self.start_datetime + dur

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this event."""
        return reverse('event-detail', args=[str(self.id)])

    def get_create_tickets_url(self):
        """Returns the url to access a detail record for this event."""
        return reverse('create-tickets', args=[str(self.id)]) + '?id=' + str(self.id)

class Ticket(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=5)#999,99 es el maximo
    category = models.CharField(max_length = 40, help_text='The name of the type of ticket you are trying to sell.',default = 'Basic')
    description = models.TextField(help_text='Decribe what this ticket entices.', default="this allows you to enter the party.")
    # ticket_id = models.CharField()#<-- podemos usar a primary key para identificarlos, este tributo es redundante.
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.category) +' '+ str(self.event)

    class Meta:
        ordering=('category','price')

class CreateTicket(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=5,default=1)#999,99 es el maximo
    category = models.CharField(max_length = 40, help_text='The name of the type of ticket you are trying to sell.',default = 'Basic')
    description = models.TextField(help_text='Decribe what this ticket entices.', default="this allows you to enter the party.")
    size = IntegerRangeField(min_value=1, max_value=50, default = 1, help_text='Number of tickets. (Max)')
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.category) +' '+ str(self.event)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=5)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    

    PRODUCT_TYPE = (
        ('r', 'refreshment'),
        ('c', 'cocktail'),
        ('s', 'shot'),
        ('b', 'beer'),
        ('w', 'wine'),
        ('k', 'snack'),
        ('h', 'hookah'),
        ('m', 'misc.'),
    )
    product_type = models.CharField(
        max_length=1,
        choices=PRODUCT_TYPE,
        blank=False,
        default='m',
        help_text='product type',
    )

    reservation_exclusive = models.BooleanField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this product."""
        return reverse('product-detail', args=[str(self.id)])

    class Meta:
        ordering=('reservation_exclusive','product_type')

class Reservation(models.Model):
    max_time = models.IntegerField(help_text="max hours after the event starts people can arrive at.", max_length=2, default=4)
    price = models.DecimalField(decimal_places=2,max_digits=5)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + ' ' + str(self.price) + ' ' + str(self.max_time)


class Rating(models.Model):
    text = models.TextField(max_length=500)
    stars = models.IntegerField(help_text='star rating 1-10')
    fecha = models.DateTimeField(default=datetime.datetime.now())
    club = models.ForeignKey(Club, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.club)+' '+str(self.stars)


class QR_Item(models.Model):
    is_used = models.BooleanField(default=False)
    #The order is used so we can find the user and give them all his QR items
    #A QR_Item can be either a product, a reservation or a ticket
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE,null=True,blank=True)
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,null=True,blank=True)

    user = models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=True)
    priv_key = models.CharField(max_length=128)
    fecha = models.DateTimeField(default=datetime.datetime.now())
    timed_out = models.BooleanField(default=False)

    def __str__(self):
        return str(self.priv_key)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this product."""
        return reverse('purchase-display', args=[str(self.id),str(self.priv_key)])

    def get_real_absolute_url(self):
        str1 = QR_Item.get_absolute_url(self)
        return str("https://clubby-sprint1.herokuapp.com")+str(str1)
