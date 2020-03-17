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

from ..forms import TicketCreateModelForm

from ..models import Club, Event, Profile, Product, Ticket

import datetime

#################
#    TICKETS    #
#################

@permission_required('clubby.is_owner')
def EventCreateTickets(request, event_id):

    club_id = Event.objects.get(pk=event_id).club_id
    user_id = Club.objects.get(pk=club_id).owner_id
    user = User.objects.get(pk=user_id)
    max = Club.objects.get(pk=club_id).max_capacity
    created = Ticket.objects.all().filter(event_id=event_id).count()
    max=max-created

    current_user = request.user

    if(current_user == user):

        if (request.method == 'POST'):
            form = TicketCreateModelForm(data=request.POST or None, max = max)
            if form.is_valid():

                size = form.cleaned_data['size']
                price = form.cleaned_data['price']
                category = form.cleaned_data['category']
                description = form.cleaned_data['description']
                t = Ticket(price=price, event_id=event_id, user_id='',category=category,description=description)
            
                for i in range(0, size):
                    t.pk = None
                    t.save()
                    i+=1

                return HttpResponseRedirect(reverse('my-events-future'))

            # return render(request, 'clubby/ticket/create.html', {'form': form})

        else:
            form = TicketCreateModelForm(initial={'price':1,'size':max,'description':'this allows you to enter the party',
                'category': 'Basic'}, max=max)
            return render(request, 'clubby/ticket/create.html', {'form': form})

    else:
        raise PermissionDenied("You don't own that >:(")

# class EventCreateTicketsView(PermissionRequiredMixin,CreateView):
#     permission_required = 'clubby.is_owner'
#     model = Ticket
#     form_class = TicketCreateModelForm #<-- since the validation is here we need to specify the form we want to use.
#     template_name = 'clubby/event/event_form.html'
#     # you can't use the exclude here.

#     # we need to overide the default method for saving in this case because we need to
#     # add the logged user as the owner to the club.

#     def form_valid(self, form):
#         id = self.request.GET.get('id')
#         u = form.cleaned_data['size']
#         price = form.cleaned_data['price']
#         category = form.cleaned_data['category']
#         description = form.cleaned_data['description']
#         t = Ticket(price=price, event_id=id, user_id='',category=category,description=description)

#         for i in range(0, u):
#             t.pk = None
#             t.save()
#             i+=1

#         return HttpResponseRedirect(reverse('my-events-future'))