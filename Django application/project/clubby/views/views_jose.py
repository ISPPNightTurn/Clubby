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

from ..forms import ProductPurchaseForm

from ..models import Club, Event, Profile, Product, Ticket, QR_Item

from django.utils.crypto import get_random_string

import datetime

#################
#    PRODUCTS    #
#################


def ProductsByClubList(request, club_id):
    if (request.method == 'POST'):
        form = ProductPurchaseForm(request.POST)
        print(form)
        if form.is_valid():
            print("Es válido")

            product_id = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            product_selected = Product.objects.filter(pk=product_id)[0]

            print(str(product_selected)+' '+str(quantity))

            user_is_broke = False
            if(product_selected.price * quantity > request.user.profile.funds):
                user_is_broke = True
            else:
                total_cost = product_selected.price * quantity
                request.user.profile.funds -= total_cost 
                request.user.save()

                owner = product_selected.club.owner
                owner.profile.funds += total_cost - (total_cost*0.05) #we take the 5% off the purchase.
                owner.save()

                for x in range(quantity):
                    qr = QR_Item(is_used=False,product=product_selected,priv_key=get_random_string(length=128),user=request.user)
                    qr.save()
            
            return render(request,'clubby/purchase/list.html',{'user_is_broke':user_is_broke})
    else:
        club = Club.objects.filter(pk=club_id)[0]
        products = Product.objects.filter(club = club)

        product_ammount=dict()
        for t in range(len(products)):
            #returns the ammount of unsold tickets for an event and category
            form = ProductPurchaseForm(initial={'product':products[t].pk})
            product_ammount[products[t]] = form

        context = {'product_ammount': product_ammount}
        return render(request,'clubby/product/list.html',context)
    
    
#################
#    QR         #
#################


class QRsByUserListView(LoginRequiredMixin, generic.ListView):
    
    permission_required = 'clubby.is_user'
    model = QR_Item
    template_name ='clubby/purchase/list.html'
    paginate_by = 5

    login_url = '/login/' #<-- as this requires identification, we specify the redirection url if an anon tries to go here.
    
    def get_queryset(self):
        item = QR_Item.objects.filter(user = self.request.user).filter(is_used=False)
        return item


class QRsUsedByUserListView(LoginRequiredMixin, generic.ListView):
    
    permission_required = 'clubby.is_user'
    model = QR_Item
    template_name ='clubby/purchase/history_list.html'
    paginate_by = 5

    login_url = '/login/' #<-- as this requires identification, we specify the redirection url if an anon tries to go here.
    
    def get_queryset(self):
        item = QR_Item.objects.filter(user = self.request.user).filter(is_used=True)
        return item


class DisplayQRItemView(generic.DetailView):
    model = QR_Item
    template_name = 'clubby/purchase/display.html'  # Specify your own template name/location