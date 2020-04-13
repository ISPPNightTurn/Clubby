from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader

from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.core.exceptions import PermissionDenied, ValidationError

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# from clubby.forms import EventAddForm
from ..forms import ClubModelForm, SignupForm, ProductModelForm, EventModelForm, FundsForm, SearchForm, SearchEventForm, SpotifyForm
from ..models import Club, Event, Profile, Product, Ticket, SecurityAdvice

from datetime import datetime, timedelta
from django.utils.translation import gettext

import urllib.parse
import datetime
import calendar
import json
import requests as rq

GOOGLE_API_KEY = 'AIzaSyDLS2DKjJkCSPc0x_2BXcxDfr8mgByTPEo'

# Create your views here.

# The views in django are sorta like DP controllers and they are the ones
# that send the variables to the paths you set on the urls.py file

###############
#   CLUBBY    #
###############

def landing(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_clubs = Club.objects.all().count()
    num_events = Event.objects.all().count()

    # Available books (status = 'a')

    # check on filtering later on.
    # num_events_future = Event.objects.filter(start_date__day >= 29).count()

    # The 'all()' is implied by default.
    num_users = User.objects.count()

    # Number of visits to this view, as counted in the session variable.
    # We can expand on sessions later on, they are used for interaction with anonymous users.
    # Sessions is actually just a python dictionary and you can do whatever you want on it.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    security_advice = SecurityAdvice.objects.filter(is_active=True)

    context = {
        'num_clubs': num_clubs,
        'num_events': num_events,
        # 'num_events_future': num_events_future,
        'num_users': num_users,
        'num_visits': num_visits,
        'security_advice':security_advice
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'clubby/landing.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = FundsForm(request.POST)

        if form.is_valid():
            to_recharge = form.cleaned_data.get('ammount')
            return redirect('add-funds', ammount=to_recharge)
        else:
            return redirect('profile')
    else:
        google_url = ""
        me = request.user  # this is the current user.
        try:
            profile = Profile.objects.filter(user=me)[0]
        except:
            profile = ''
        try:
            club = Club.objects.filter(owner=me)[0]
            google_url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(club.latitude)+","+str(club.longitude)+"&markers=color:red%7Clabel:C%7C"+str(club.latitude)+","+str(club.longitude)+"&zoom=13&size=600x300&maptype=roadmap&key="+ GOOGLE_API_KEY
        except:
            club = ''
            
        form = FundsForm()

        client_id ='7af4e7e36a454ec09746fa13559947d9'
        redirect_uri = 'http://localhost:8000/clubby/spotify/authorize/'
        scope = 'user-top-read'

        spotify_link_url = 'https://accounts.spotify.com/authorize?client_id='+client_id+'&response_type=code&redirect_uri='+redirect_uri+'&scope=user-top-read&show_dialog=true'

        context = {'logged_user': me, 'user_profile': profile,
                   'club': club, 'form': form, 'google_url': google_url, 'spotify_url':spotify_link_url}
        return render(request, 'clubby/profile.html', context)

# we not only register the user but also authenticate them.


def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.funds = 0.0
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            my_group = Group.objects.get(name='user')
            my_group.user_set.add(user)

            return redirect('landing')
    else:
        form = SignupForm()
    return render(request, 'clubby/signup.html', {'form': form, 'user': True, 'owner': False})


def signup_owner(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.funds = 0.0
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            my_group = Group.objects.get(name='owner')
            my_group.user_set.add(user)

            return redirect('landing')
    else:
        form = SignupForm()
    return render(request, 'clubby/signup.html', {'form': form, 'owner': True, 'user': False})


###############
#    CLUB     #
###############

class ClubListView(generic.ListView):
    paginate_by = 5  # add pagination to the view
    model = Club
    # Specify your own template name/location
    template_name = 'clubby/club/list.html'
        
    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)
        form = SearchForm()
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        form = SearchForm(self.request.POST)
        query = form['query'].value()
        items = Club.objects.all()

        clubs = []
        for club in items:
            if((query.lower() in club.name.lower()) or (query.lower() in club.address.lower())):
                clubs.append(club)

        return render(request, 'clubby/club/list.html', {'object_list': clubs, 'form': form})


class ClubListCloseByView(generic.ListView):
    paginate_by = 5  # add pagination to the view
    model = Club
    # Specify your own template name/location
    template_name = 'clubby/club/list_nearby.html'

    def get_queryset(self):
        latitude, longitude = None, None
        try:
            latitude = self.request.GET.get("latitude")
            longitude = self.request.GET.get("longitude")

            #1 degree is 111KM

            min_lat = float(latitude)-0.1
            max_lat = float(latitude)+0.1

            min_lng = float(longitude)-0.1
            max_lng = float(longitude)+0.1

            items = Club.objects.filter(latitude__gte = min_lat).filter(latitude__lte = max_lat).filter(longitude__gte = min_lng).filter(longitude__lte = max_lng)

            return items
        except:
            print('no geolocation information recieved.')
            items = Club.objects.all()
            return items
        
    def get_context_data(self, **kwargs):
        context = super(ClubListCloseByView, self).get_context_data(**kwargs)

        latitude, longitude = None, None
        try:
            latitude = self.request.GET.get("latitude")
            longitude = self.request.GET.get("longitude")
        except:
            print('no geolocation information recieved.')

        if(latitude != None and longitude != None):
            context['location_passed'] = 'true'
        else:
            context['location_passed'] = 'false'

        return context



class ClubDetailView(generic.DetailView):
    model = Club
    # Specify your own template name/location
    template_name = 'clubby/club/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        context['google_url'] = 'https://www.google.com/maps/embed/v1/search?q='+urllib.parse.quote(self.object.address)+'&key='+GOOGLE_API_KEY
        return context
    
class ClubCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'clubby.is_owner'
    model = Club
    # <-- since the validation is here we need to specify the form we want to use.
    form_class = ClubModelForm
    template_name = 'clubby/club/club_form.html'
    # you can't use the exclude here.

    # we need to overide the default method for saving in this case because we need to
    # add the logged user as the owner to the club.
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user

        club_address = form.cleaned_data.get('address')
        club_address = club_address.replace(" ","+")
        club_address = club_address.replace(",",",+")

        #'1600+Amphitheatre+Parkway,+Mountain+,View,+CA'
        response = rq.request('GET','https://maps.googleapis.com/maps/api/geocode/json?address='+club_address+'&key='+GOOGLE_API_KEY)
        json_data = json.loads(response.text)

        dictionary = json_data['results'][0]['geometry']['location']
        obj.latitude = dictionary['lat']
        obj.longitude = dictionary['lng']
                
        # this is neccesary as the url is pulled from self.object.
        self.object = obj
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class ClubUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'clubby.is_owner'
    model = Club
    form_class = ClubModelForm
    template_name = 'clubby/club/club_form.html'
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if(self.object.owner != request.user):
            raise PermissionDenied("You don't own that >:(")
        else:
            return super(ClubUpdate, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        # this is neccesary as the url is pulled from self.object.
        self.object = obj

        club_address = form.cleaned_data.get('address')
        club_address = club_address.replace(" ","+")
        club_address = club_address.replace(",",",+")

        #'1600+Amphitheatre+Parkway,+Mountain+,View,+CA'
        response = rq.request('GET','https://maps.googleapis.com/maps/api/geocode/json?address='+club_address+'&key='+GOOGLE_API_KEY)
        json_data = json.loads(response.text)

        dictionary = json_data['results'][0]['geometry']['location']
        obj.latitude = dictionary['lat']
        obj.longitude = dictionary['lng']

        if(obj.owner == self.request.user):
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise PermissionDenied("You don't own that >:(")

class ClubDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'clubby.is_owner'
    model = Club
    template_name = 'clubby/club/club_confirm_delete.html'
    success_url = reverse_lazy('clubs')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if(self.object.owner != request.user):
            raise PermissionDenied("You don't own that >:(")
        else:
            return super(ClubDelete, self).get(request, *args, **kwargs)

    # to check for permissions we override the default delete method
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        can_delete = self.object.owner == self.request.user

        if can_delete:
            return super(ClubDelete, self).delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("You don't own that >:(")

#################
#    PRODUCT    #
#################


class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'clubby.is_owner'
    model = Product
    # <-- since the validation is here we need to specify the form we want to use.
    form_class = ProductModelForm
    template_name = 'clubby/product/product_form.html'
    # you can't use the exclude here.

    # we need to overide the default method for saving in this case because we need to
    # add the logged user as the owner to the club.
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.club = self.request.user.club
        # this is neccesary as the url is pulled from self.object.
        self.object = obj
        obj.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class ProductsByClubListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing events the user has participated, or is going to participate in."""
    model = Product
    template_name = 'clubby/product/list.html'
    paginate_by = 5

    # <-- as this requires identification, we specify the redirection url if an anon tries to go here.

    def get_queryset(self):
        item = Product.objects.filter(club=self.request.user.club)
        return item

#################
#     EVENT     #
#################

# Generic view for displaying all events.


class EventListView(generic.ListView):
    paginate_by = 5
    model = Event
    # context_object_name = 'my_event_list'   # your own name for the list as a template variable
    # Specify your own template name/location
    template_name = 'clubby/event/list.html'

    def get_queryset(self):
        # gte = greater than or equal.
        # gt = greater than
        # lte = lesser than or equal
        # lt = lesser than
        items = Event.objects.filter(start_date__gte=datetime.datetime.now().date()).order_by('start_date', 'start_time')
        return items

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)

        end_date = datetime.datetime.now()+datetime.timedelta(days=7)
        start_date = datetime.datetime.now()

        

        form = SearchEventForm(
            initial={'end_date': end_date.date().strftime("%Y-%m-%d"), 'start_date': start_date.date().strftime("%Y-%m-%d")})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = SearchEventForm(self.request.POST)

        start_date = form['start_date'].value()
        end_date = form['end_date'].value()
        # check if these were used.
        items = Event.objects.filter(start_date__gte=start_date)
        items = items.filter(start_date__lte=end_date).order_by(
            'start_date', 'start_time')
        items = items.filter(start_date__gte=datetime.datetime.now())

        return render(request, 'clubby/event/list.html', {'object_list': items, 'form': form})
        # return StatusFormView.as_view()(request)


class EventDetailView(generic.DetailView):
    model = Event
    # Specify your own template name/location
    template_name = 'clubby/event/detail.html'

# we should make a new view for this due to pagination bugs, but the filtering works.
# we can also call the required mixin to our own defined views but we need to declare them first, same as @login_required.


class EventsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing events the user has participated, or is going to participate in."""
    model = Event
    template_name = 'clubby/event/user_list.html'
    paginate_by = 5
    # <-- as this requires identification, we specify the redirection url if an anon tries to go here.

    def get_queryset(self):

        list = Event.objects.filter(atendees=self.request.user).order_by(
            '-start_date', '-start_time')
        return list


class EventsByClubAndFutureListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing events of the club, that haven't happened yet."""
    permission_required = 'clubby.is_owner'
    model = Event
    template_name = 'clubby/event/future-list.html'
    paginate_by = 5
    # <-- as this requires identification, we specify the redirection url if an anon tries to go here.

    def get_queryset(self):
        # the gte and lte indicate greater than and lesser than for filtering by dates.
        club = Club.objects.filter(owner=self.request.user)[0]
        list = Event.objects.filter(start_date__gte=datetime.datetime.now(
        ).date()).filter(club=club).order_by('-start_date', '-start_time')
        return list


class EventCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'clubby.is_owner'
    model = Event
    # <-- since the validation is here we need to specify the form we want to use.
    form_class = EventModelForm
    template_name = 'clubby/event/event_form.html'
    # you can't use the exclude here.

    def form_valid(self, form):
        duration = form.cleaned_data.get('duration')
        start_time = form.cleaned_data.get('start_time')
        start_date = form.cleaned_data.get('start_date')

        now = datetime.datetime.now().date()
        errors = []

        if(start_date < now):
            errors.append('date cant be in the past.')

        if(start_time > 24 or start_time < 0):
            errors.append('start time is invalid')

        if(duration > 12 or duration < 0):
            errors.append('Duration is invalid')

        if(len(errors) != 0):
            return render(self.request, 'clubby/event/event_form.html', {'form': form, 'errors': errors})

        owner = self.request.user

        now = datetime.datetime.now()
        lastday = calendar.monthrange(now.year, now.month)[1]
        first = datetime.datetime(now.year, now.month, 1)
        last = datetime.datetime(now.year, now.month, lastday)

        events_in_month = Event.objects.filter(club=owner.club).filter(
            start_date__gte=first).filter(start_date__lte=last).count()
        # commit false avoids the object being saved to the database directly:
        obj = form.save(commit=False)
        obj.owner = owner
        obj.club = obj.owner.club
        # this is neccesary as the url is pulled from self.object.
        self.object = obj
        if(events_in_month < 2):
            obj.save()
        else:
            if(owner.groups.filter(name='premium owner').exists()):
                obj.save()
            else:
                form = FundsForm()
                context = {'logged_user': owner, 'user_profile': owner.profile,
                           'club': owner.club, 'form': form, 'over_event_limit': True}
                return render(self.request, 'clubby/profile.html', context)

        return HttpResponseRedirect(self.object.get_create_tickets_url())
