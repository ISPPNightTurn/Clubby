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
from django import forms

from django.utils.crypto import get_random_string

from ..forms import TicketPurchaseForm, FundsForm, PremiumForm, SearchForm, EditProfileForm
from ..models import Club, Event, Profile, Product, Ticket, QR_Item

from background_task.models import Task

from ..tasks import check_premium

from django.conf import settings
import datetime
from decimal import Decimal
import stripe # new
stripe.api_key = settings.STRIPE_SECRET_KEY # new


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
    if (request.method == 'POST'): # ha elegido la cantidad de tickets tipo que queria.
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event']
            category = form.cleaned_data['category']
            quantity = form.cleaned_data['quantity']
            if (quantity > 4):
                quantity = 4 # max you can purchase

            logged = request.user
            event = Event.objects.filter(pk=event_id)[0]
            num_tickets_user_event = Ticket.objects.filter(event = event).filter(user=logged).count()

            max_purchasable = 4 - num_tickets_user_event
            max_tickets = False
            if(quantity > max_purchasable):
                max_tickets = True
                quantity = max_purchasable

            missing_tickets = False
            miss = 0
            user_is_broke = False
            if(not max_tickets):
                tickets_from_db = Ticket.objects.filter(event = event).filter(user = None).filter(category=category)
                to_buy = len(tickets_from_db) if (len(tickets_from_db) <= quantity) else quantity

                print(str(to_buy) + str(tickets_from_db))
                
                total_cost = tickets_from_db[0].price * to_buy
                if (total_cost>logged.profile.funds):
                    user_is_broke = True
                else:
                    logged.profile.funds -= (total_cost* to_buy)
                    logged.profile.save()

                    owner = event.club.owner
                    owner.profile.funds += total_cost - total_cost*Decimal("0.05") #we take the 5% off the purchase.
                    owner.save()
                    
                    for x in range(to_buy):
                        tick = tickets_from_db[x]
                        tick.user = logged
                        tick.save()
                        tick.refresh_from_db()

                        qr = QR_Item(is_used=False,priv_key=get_random_string(length=128),user=logged,ticket=tick,
                            fecha=datetime.datetime.now(), timed_out=False)
                        qr.save()
                        
                    event.atendees.add(request.user)
                    # event.save() no need to save as add saves it for us.

            context = {'event':event,'missing_tickets':missing_tickets,'miss':miss,'max_tickets':max_tickets,'user_is_broke':user_is_broke}
            return render(request,'clubby/event/detail.html',context)
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

###############
#    FUNDS    #
###############

@login_required
def add_funds(request, ammount):
    form = FundsForm()
    form.initial['ammount'] = int(ammount * 100)
    form.fields['ammount'].widget = forms.HiddenInput()
    return render(request, 'clubby/funds.html', {'form': form, 'key': settings.STRIPE_PUBLISHABLE_KEY,'ammount':int(ammount * 100)})

@login_required
def charge(request, ammount): # new
    if request.method == 'POST':
        form = FundsForm(request.POST)
        ammount = form['ammount'].value()

        # form.is_valid()
        # print (form)

        # ammount = form.cleaned_data['ammount']
        # print('I get here.')

        charge = stripe.Charge.create(
        amount=int(ammount),
        currency='usd',
        description='A Django charge',
        source=request.POST['stripeToken']
    )

        profile = request.user.profile
        profile.funds += Decimal(str(int(ammount)/100))
        profile.save()

        return render(request,'clubby/charge.html')
        # else:
        #     print(form)
        #     return render(request,'clubby/charge.html')

#################
#    PREMIUM    #
#################
@permission_required('clubby.is_owner')
def get_premium(request): # new
    if request.method == 'POST':
        form = PremiumForm(request.POST)
        has_accepted = form['accept'].value()
        if(has_accepted):
            owner = request.user
            
            if(owner.profile.funds < Decimal("15")):
                return render(request,'clubby/premium.html',{'form':form,'not_enough_funds':True})
            else:
                # These are models created by the django-background-tasks package...
                owner_tasks = Task.objects.filter(creator_object_id=owner.pk)
                profile = owner.profile

                print(owner_tasks)

                if(len(owner_tasks)==0):
                    profile.renew_premium = True
                    profile.funds -=  Decimal("15")
                    my_group = Group.objects.get(name='premium owner') 
                    my_group.user_set.add(owner)
                    owner.save()
                    profile.save()
                    now = datetime.datetime.now()
                    if(now.month == 12):
                        next_payment = datetime.datetime(now.year+1, 1 , 2, 2)
                    else:
                        next_payment = datetime.datetime(now.year,now.month +1 , 2, 2)

                    #check_premium(owner.pk, schedule=next_payment, creator=owner) #Solo la crearemos una vez.
                    check_premium(owner.pk, schedule=600, creator=owner) #10 Minutos como testing.
                else:
                    profile.funds -=  Decimal("15")
                    profile.renew_premium = True
                    profile.save()

                #check_premium(owner.pk, schedule=60)
                return render(request,'clubby/charge.html')
        else:
            return render(request,'clubby/premium.html',{'form':form,'not_accepted':True})
    else:
        form = PremiumForm(initial={'accept':False})
        return render(request,'clubby/premium.html',{'form':form})

@permission_required('clubby.is_premium_owner')
def cancel_premium(request):
    if request.method == 'POST':
        form = PremiumForm(request.POST)
        has_accepted = form['accept'].value()
        if(has_accepted):
            owner = request.user
            profile = owner.profile    
            profile.funds -=  Decimal("15")
            profile.renew_premium = False
            my_group = Group.objects.get(name='premium owner') 
            my_group.user_set.remove(owner)
            profile.save()
            return render(request,'clubby/charge.html')
        else:
            return render(request,'clubby/cancel_premium.html',{'form':form,'not_accepted':True})
    else:
        form = PremiumForm(initial={'accept':False})
        return render(request,'clubby/cancel_premium.html',{'form':form})
    
########################
#    EDIT USER DATA    #
########################

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request=request)
        if form.is_valid():
            user = request.user
            profile = user.profile
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')

            user.save()

            profile.birth_date = form.cleaned_data.get('birth_date')
            profile.bio = form.cleaned_data.get('bio')
            profile.location = form.cleaned_data.get('location')
            profile.picture = form.cleaned_data.get('picture')

            profile.save()
            return redirect('profile')
        else:
            return render(request,'clubby/edit_profile.html',{'form':form})
    else:
        user = request.user
        form = EditProfileForm(initial={'first_name':user.first_name,'last_name':user.last_name,'email':user.email,
        'bio':user.profile.bio, 'location':user.profile.location, 'birth_date':user.profile.birth_date,})
        return render(request,'clubby/edit_profile.html',{'form':form})
