from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader

from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.core.exceptions import PermissionDenied

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# from clubby.forms import EventAddForm
from .forms import ClubModelForm, SignupForm,ProductModelForm,EventModelForm

from .models import Club, Event, Profile, Product 

import datetime


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
    
    context = {
        'num_clubs': num_clubs,
        'num_events': num_events,
        #'num_events_future': num_events_future,
        'num_users': num_users,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'clubby/landing.html', context=context)

@login_required
def profile(request):
    me = request.user #this is the current user.
    try:
        profile = Profile.objects.filter(user=me)[0]
    except:
        profile = ''

    try:
        club = Club.objects.filter(owner=me)[0]
    except:
        club = ''
    
    context = {'logged_user': me,'user_profile': profile, 'club':club}
    return render(request,'clubby/profile.html',context)

# we not only register the user but also authenticate them.
def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            my_group = Group.objects.get(name='user') 
            my_group.user_set.add(user)
            return redirect('landing')
    else:
        form = SignupForm()
    return render(request, 'clubby/signup.html', {'form': form, 'user':True, 'owner':False})

def signup_owner(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            my_group = Group.objects.get(name='owner') 
            my_group.user_set.add(user)
            return redirect('landing')
    else:
        form = SignupForm()
    return render(request, 'clubby/signup.html', {'form': form, 'owner':True, 'user':False})

# this would be a custom view for form treatment. come back to it later on...

# @permission_required('clubby.can_add_event') # <-- only owners
# def add_event(request):
#     """View function for adding an event to a club."""
#     me = request.user
#     club = get_object_or_404(Club, owner=me)
#     event = Models
#     # if owner doesnt have a club we should send him to the create club view. (this shouldn't happen?)

#     # If this is a POST request then process the Form data (something went wrong)
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = EventAddForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             event.start_date = form.cleaned_data['event_date']
#             club.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('all-borrowed') )

#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

#     context = {
#         'form': form,
#         'club': club,
#     }

#     return render(request, 'clubby/event/add.html', context)


# Generic views are the way that django makes easy the processing of simple requests:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
# you can see more about them here


###############
#    CLUB     #
###############

class ClubListView(generic.ListView):
    paginate_by = 2 # add pagination to the view
    model = Club
    template_name = 'clubby/club/list.html'  # Specify your own template name/location 

class ClubDetailView(generic.DetailView):
    model = Club
    template_name = 'clubby/club/detail.html'  # Specify your own template name/location
    #investigate how to add a list of all events that belong to the club.

# Generic views are the same as list vies but for editing the models:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# see more here

class ClubCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'clubby.is_owner'
    model = Club
    form_class = ClubModelForm #<-- since the validation is here we need to specify the form we want to use.
    template_name = 'clubby/club/club_form.html'
    # you can't use the exclude here.

    # we need to overide the default method for saving in this case because we need to
    # add the logged user as the owner to the club.
    def form_valid(self, form):  
        obj = form.save(commit=False)
        obj.owner = self.request.user
        self.object = obj # this is neccesary as the url is pulled from self.object.
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

class ClubUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'clubby.is_owner'
    model = Club
    template_name = 'clubby/club/club_form.html'
    fields = ['name', 'address', 'max_capacity', 'NIF']

    def form_valid(self, form):  
        obj = form.save(commit=False)
        self.object = obj # this is neccesary as the url is pulled from self.object.
        if(obj.owner == self.request.user):
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise PermissionDenied("You don't own that >:(")



class ClubDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'clubby.is_owner'
    model = Club
    template_name = 'clubby/club/club_confirm_delete.html'
    success_url = reverse_lazy('clubs')

    def delete(self, request, *args, **kwargs): #to check for permissions we override the default delete method
        self.object = self.get_object()
        can_delete = self.object.owner == self.request.user

        if can_delete:
            return super(ClubDeleteView, self).delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("You don't own that >:(")

#################
#    PRODUCT    #
#################
class ProductCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'clubby.is_owner'
    model = Product
    form_class = ProductModelForm #<-- since the validation is here we need to specify the form we want to use.
    template_name = 'clubby/product/product_form.html'
    # you can't use the exclude here.

    # we need to overide the default method for saving in this case because we need to
    # add the logged user as the owner to the club.
    def form_valid(self, form):  
        obj = form.save(commit=False)
        obj.owner = self.request.user
        self.object = obj # this is neccesary as the url is pulled from self.object.
        obj.save()
        return HttpResponseRedirect(reverse('my-products'))

class ProductsByClubListView(LoginRequiredMixin, generic.ListView):
        """Generic class-based view listing events the user has participated, or is going to participate in."""
        model = Product
        template_name ='clubby/product/list.html'
        paginate_by = 2

        login_url = '/login/' #<-- as this requires identification, we specify the redirection url if an anon tries to go here.
    
        def get_queryset(self):
            item = Product.objects.filter(club = self.request.user.club)#.filter(status__exact='o').order_by('due_back')
            return item

#################
#     EVENT     #
#################

# Generic view for displaying all events.
class EventListView(generic.ListView):
    paginate_by = 2
    model = Event
    #context_object_name = 'my_event_list'   # your own name for the list as a template variable
    template_name = 'clubby/event/list.html'  # Specify your own template name/location

    # we override the default to get events that have the year over 2020.
    # def get_queryset(self):
    #     return Event.objects.filter(start_date__year >= 2020)[:5] # Get 5 events with year 2020 or more.

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'clubby/event/detail.html'  # Specify your own template name/location

# we should make a new view for this due to pagination bugs, but the filtering works.
# we can also call the required mixin to our own defined views but we need to declare them first, same as @login_required.
class EventsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing events the user has participated, or is going to participate in."""
    model = Event
    template_name ='clubby/event/list.html'
    paginate_by = 5

    login_url = '/login/' #<-- as this requires identification, we specify the redirection url if an anon tries to go here.
    
    def get_queryset(self):
        item = Event.objects.filter(atendees = self.request.user)#.filter(status__exact='o').order_by('due_back')
        return item

class EventsByClubListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing events the user has participated, or is going to participate in."""
    model = Event
    template_name ='clubby/event/list.html'
    paginate_by = 5

    login_url = '/login/' #<-- as this requires identification, we specify the redirection url if an anon tries to go here.
    
    def get_queryset(self):
        item = Event.objects.filter(club = self.request.user.club)#.filter(status__exact='o').order_by('due_back')
        return item

class EventCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'clubby.is_owner'
    model = Event
    form_class = EventModelForm #<-- since the validation is here we need to specify the form we want to use.
    template_name = 'clubby/event/event_form.html'
    # you can't use the exclude here.

    # we need to overide the default method for saving in this case because we need to
    # add the logged user as the owner to the club.
    def form_valid(self, form):  
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.club = obj.owner.club
        self.object = obj # this is neccesary as the url is pulled from self.object.
        obj.save()
        return HttpResponseRedirect(reverse('my-events'))

##########################
#    EXAMPLES (POLLS)    #
##########################

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'clubby/polls/index.html', context)

#     # Both of these do the same but django offers the render() option for easyness

#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('clubby/index.html')
#     # context = {
#     #     'latest_question_list': latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'clubby/polls/detail.html', {'question': question})

#     # get_list_or_404() <-- this is a similar function but instead of returning the 404 if the id...
#     # is not found it returns it if the list is empty.

#     # Both of these do the same but django offers the get_object_or_404() option for easyness

#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'clubby/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'clubby/polls/results.html', {'question': question})

# # All the information about how to process a form can be found here including 
# # everything you can find in this function
# # https://docs.djangoproject.com/en/3.0/intro/tutorial04/#write-a-minimal-form

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'clubby/polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('clubby:polls-results', args=(question.id,)))




