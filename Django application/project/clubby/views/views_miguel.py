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

from ..forms import TicketPurchaseForm

from ..models import Club, Event, Profile, Product, Ticket

import datetime

class ProductDetailView(LoginRequiredMixin,generic.DetailView):
    model = Product
    template_name = 'clubby/product/detail.html'  # Specify your own template name/location
    
    #investigate how to add a list of all events that belong to the club.

class ProductUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'clubby.is_owner'
    model = Product
    template_name = 'clubby/product/product_form.html'
    fields = ['name','price']

    def form_valid(self, form):  
        obj = form.save(commit=False)
        self.object = obj # this is neccesary as the url is pulled from self.object.
        if(obj.club.owner == self.request.user):
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise PermissionDenied("You don't own that >:(")

class ProductDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'clubby.is_owner'
    model = Product
    template_name = 'clubby/product/product_confirm_delete.html'
    success_url = reverse_lazy('my-products')

    def delete(self, request, *args, **kwargs): #to check for permissions we override the default delete method
        self.object = self.get_object()
        can_delete = self.object.club.owner == self.request.user

        if can_delete:
            return super(ProductDelete, self).delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("You don't own that >:(")

#################
#    TICKETS    #
#################

@permission_required('clubby.is_user')
def TicketsByEventList(request, event_id):
    if (request.method == 'POST'): # ha elegido la cantidad de entradas del tipo que queria.
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event']
            category = form.cleaned_data['category']
            quantity = form.cleaned_data['quantity']
            event = Event.objects.filter(pk=event_id)[0]

            print(str(event)+' '+str(category) +' '+str(quantity))

            tickets_from_db = Ticket.objects.filter(event = event).filter(user = None).filter(category=category)
            missing_tickets = False
            miss = 0
            len(tickets_from_db)
            for x in range(quantity):
                try:
                    tickets_from_db[x].user = request.user
                    tickets_from_db[x].save()
                except:
                    missing_tickets = True
                    miss += 1

            print(request.user)
            print(event.atendees)

            event.atendees.add(request.user)
            # event.save()

            return render(request,'clubby/event/detail.html',{'event':event,'missing_tickets':missing_tickets,'miss':miss})
    else:
        event = Event.objects.filter(pk=event_id)[0]
        tickets_from_db = Ticket.objects.filter(event = event).filter(user = None)

        categories = []
        tickets = []
        for t in tickets_from_db:
            if (t.category not in categories):
                categories.append(t.category)
                tickets.append(t)

        ticket_ammount = dict()
        for t in range(len(tickets)):
            #returns the ammount of unsold tickets for an event and category
            form = TicketPurchaseForm(initial={'event':event.pk,'category':categories[t]})
            ticket_ammount[tickets[t]] = form

        context = {'ticket_ammount': ticket_ammount}
        return render(request,'clubby/ticket/list.html',context)