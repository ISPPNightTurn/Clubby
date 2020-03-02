from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

from .models import Choice, Question
from .models import Club, Event, Profile 
from django.template import loader

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

# Generic views are the way that django makes easy the processing of simple requests:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
# you can see more about them here

from django.views import generic

class ClubListView(generic.ListView):
    paginate_by = 2 # add pagination to the view
    model = Club
    template_name = 'clubby/club/list.html'  # Specify your own template name/location 

class ClubDetailView(generic.DetailView):
    model = Club
    template_name = 'clubby/club/detail.html'  # Specify your own template name/location
    #investigate how to add a list of all events that belong to the club.

# Generic view for displaying all events.
class EventListView(generic.ListView):
    paginate_by = 2
    model = Event
    context_object_name = 'my_event_list'   # your own name for the list as a template variable
    template_name = 'clubby/event/list.html'  # Specify your own template name/location

    # we override the default to get events that have the year over 2020.
    # def get_queryset(self):
    #     return Event.objects.filter(start_date__year >= 2020)[:5] # Get 5 events with year 2020 or more.

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'clubby/event/detail.html'  # Specify your own template name/location

# we should make a new view for this due to pagination bugs, but the filterint works.
class EventsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing events the user has participated, or is going to participate in."""
    model = Event
    template_name ='clubby/event/list.html'
    paginate_by = 2
    
    def get_queryset(self):
        return Event.objects.filter(atendees = self.request.user)#.filter(status__exact='o').order_by('due_back')

#################
#   EXAMPLES    #
#################
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'clubby/polls/index.html', context)

    # Both of these do the same but django offers the render() option for easyness

    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('clubby/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'clubby/polls/detail.html', {'question': question})

    # get_list_or_404() <-- this is a similar function but instead of returning the 404 if the id...
    # is not found it returns it if the list is empty.

    # Both of these do the same but django offers the get_object_or_404() option for easyness

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'clubby/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'clubby/polls/results.html', {'question': question})

# All the information about how to process a form can be found here including 
# everything you can find in this function
# https://docs.djangoproject.com/en/3.0/intro/tutorial04/#write-a-minimal-form

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'clubby/polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('clubby:polls-results', args=(question.id,)))




