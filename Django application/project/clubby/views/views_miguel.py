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
#from ..forms import ClubModelForm, SignupForm,ProductModelForm,EventModelForm

from ..models import Club, Event, Profile, Product 

import datetime

class ProductCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'clubby.is_owner'
    model = Product
    fields = ['name','price']
    template_name = 'clubby/product/product_form.html'
    # you can't use the exclude here.

    # we need to overide the default method for saving in this case because we need to
    # add the logged user as the owner to the club.
    def form_valid(self, form):  
        obj = form.save(commit=False)
        obj.club = self.request.user.club
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