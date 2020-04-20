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

from ..forms import ProductPurchaseForm, RedeemQRCodeForm

from ..models import Club, Event, Profile, Product, Ticket, QR_Item, Rating

from django.utils.crypto import get_random_string

from datetime import datetime, timedelta
from django.utils.translation import gettext

from decimal import Decimal
import qr_code
import csv

import datetime
import pytz
from django.utils import timezone
from django.utils.translation import gettext as _



#################
#    PRODUCTS    #
#################


def ProductsByClubList(request, club_id):
    if (request.method == 'POST'):
        form = ProductPurchaseForm(request.POST)
        if form.is_valid():
            

            product_id = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            product_selected = Product.objects.filter(pk=product_id)[0]

            print(str(product_selected)+' '+str(quantity))

            user_is_broke = False
            if(product_selected.price * quantity > request.user.profile.funds):
                user_is_broke = True
                
                item = QR_Item.objects.filter(user = request.user).filter(is_used=False).filter(expiration_date__gte=datetime.datetime.now()).order_by('-fecha')
                return render(request,'clubby/purchase/list.html',{'user_is_broke':user_is_broke,'object_list':item,'now':datetime.datetime.now()})
            else:
                total_cost = product_selected.price * quantity
                request.user.profile.funds -= total_cost 
                request.user.save()

                owner = product_selected.club.owner
                owner.profile.funds += total_cost - total_cost * Decimal("0.05") #we take the 5% off the purchase.
                owner.save()

                for x in range(quantity):
                    qr = QR_Item(is_used=False,product=product_selected,priv_key=get_random_string(length=16),user=request.user,
                        fecha=datetime.datetime.now(), expiration_date=datetime.datetime.now() + timedelta(hours=6))
                    qr.save()

                return HttpResponseRedirect(reverse('purchase-confirm'))

    else:
        club = Club.objects.filter(pk=club_id)[0]
        products = Product.objects.filter(club = club)

        product_ammount=dict()
        for t in range(len(products)):

            # collect number of owned items
            products[t].owned = QR_Item.objects.filter(product_id = products[t].id).filter(
                user_id = request.user.id).filter(is_used = 0).filter(expiration_date__gt = datetime.datetime.now()).count

            #returns the ammount of unsold tickets for an event and category
            form = ProductPurchaseForm(initial={'product':products[t].pk})
            product_ammount[products[t]] = form

        context = {'product_ammount': product_ammount}
        return render(request,'clubby/product/list.html',context)
    
    
#################
#    QR         #
#################


class QRsByUserListView(PermissionRequiredMixin, generic.ListView):
    
    permission_required = 'clubby.is_user'
    model = QR_Item
    template_name ='clubby/purchase/list.html'
    paginate_by = 20

    login_url = '/login/' #<-- as this requires identification, we specify the redirection url if an anon tries to go here.
    
    def get_queryset(self):

        current_user =  self.request.user
        

        
        item = QR_Item.objects.filter(user = self.request.user).filter(is_used=False).filter(expiration_date__gte = datetime.datetime.now()).order_by('-fecha')
        return item





#class DisplayQRItemView(generic.DetailView):
   # model = QR_Item
   # template_name = 'clubby/purchase/display.html'  # Specify your own template name/location

def QRItemView(request, qr_item_id, priv_key):
    qr = QR_Item.objects.filter(pk=qr_item_id)[0]

    if(priv_key == qr.priv_key):
        context = {'qr_item':qr,}
        return render(request,'clubby/purchase/display-qr.html',context)
    else:
        raise PermissionDenied(_('the security key did not match, trying to screw people over huh? Naughty >:('))

@permission_required('clubby.is_owner')
def DisplayQRItemView(request, qr_item_id, priv_key):
    if (request.method == 'POST'):
        form = RedeemQRCodeForm(request.POST)

        if form.is_valid():
            form.cleaned_data['qr_item_id']
            qr_selected = QR_Item.objects.filter(pk=qr_item_id)[0]

            qr_selected.is_used = True
            qr_selected.save()

            return render(request,'clubby/landing.html')
    else:
            qr = QR_Item.objects.filter(pk=qr_item_id)[0]
            if(qr.ticket!=None):
                club = qr.ticket.event.club
            else:
                club = qr.product.club
            if(priv_key == qr.priv_key and request.user.club == club):

                form = RedeemQRCodeForm()
                form.initial['qr_item_id'] = qr.pk
                is_expired = qr.expiration_date < timezone.now()
                if(qr.ticket!=None):
                    is_same_day =  qr.ticket.event.start_date == datetime.datetime.today().date()
                    print(qr.ticket.event.start_date)
                    print(datetime.datetime.today())
                else:
                    is_same_day=True
                context = {'qr_item':qr,'form':form,'now':datetime.datetime.now(),'is_same_day':is_same_day,'is_expired':is_expired}

                return render(request,'clubby/purchase/display.html',context)
            else:
                raise PermissionDenied(_('the security key did not match, trying to screw people over huh? Naughty >:('))


@login_required(login_url="/login")
def socialsuccess(request):
    defaultgroup = Group.objects.get(name = 'user')
    user = request.user
    user.groups.add(defaultgroup)

    return render(request, 'clubby/landing.html') 

def terms(request):
    return render(request, 'clubby/terms.html')

def privacy(request):
    return render(request, 'clubby/privacy.html')

def privacidad(request):
    return render(request, 'clubby/privacidad.html')

def terminos(request):
    return render(request, 'clubby/terminos.html')


@login_required
def export(request):
    me = request.user  # this is the current user.
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Bio','Location','Birth Date','Picture','Username','Email','First name','Last name'])
    writer.writerow([me.profile.bio,me.profile.location,me.profile.birth_date,me.profile.picture,me.username,me.email, me.first_name,me.last_name])
    

    response['Content-Disposition'] = 'attachment;filename="member.csv"'
   
    
    return response

@login_required
def delete(request):
    me = request.user
    try:
        me.delete()
    except:
        messages.error(request, _("Something went wrong")) 
    return render(request, 'clubby/success.html')

@login_required
def purchase_confirm(request):
    return render(request,'clubby/purchaseConfirm.html')