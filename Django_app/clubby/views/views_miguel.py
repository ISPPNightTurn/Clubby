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
from django.utils.translation import gettext as _

from django.utils.crypto import get_random_string

from django.db.models import Q

from ..forms import TicketPurchaseForm, FundsForm, PremiumForm, SearchForm, EditProfileForm, ProductModelForm, SpotifyForm
from ..models import Club, Event, Profile, Product, Ticket, QR_Item, Rating

from django.utils.translation import ugettext_lazy as _
from background_task.models import Task

from ..tasks import check_premium

from django.conf import settings
from decimal import Decimal
from django.utils.translation import gettext
import datetime
import random
import json
import stripe # new
import requests
import urllib
import pytz

stripe.api_key = settings.STRIPE_SECRET_KEY # new

class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    # Specify your own template name/location
    template_name = 'clubby/product/detail.html'

    # investigate how to add a list of all events that belong to the club.


@permission_required('clubby.is_owner')
def ProductUpdate(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductModelForm(instance=product, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'clubby/product/product_form.html', {'form': form})
    else:
        form = ProductModelForm(instance=product, initial={'name': product.name, 'price': product.price,
                                                           'product_type': product.product_type, 'reservation_exclusive': product.reservation_exclusive})
        if(product.club.owner != request.user):
            raise PermissionDenied(_("You don't own that >:("))
        else:
            return render(request,'clubby/product/product_form.html',{'form':form})
        

class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'clubby.is_owner'
    model = Product
    template_name = 'clubby/product/product_confirm_delete.html'
    success_url = reverse_lazy('my-products')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if(self.object.club.owner != request.user):
            raise PermissionDenied(_("You don't own that >:("))
        else:
            return super(ProductDelete, self).get(request, *args, **kwargs)

    # to check for permissions we override the default delete method
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        can_delete = self.object.club.owner == self.request.user

        if can_delete:
            return super(ProductDelete, self).delete(request, *args, **kwargs)
        else:
            raise PermissionDenied(_("You don't own that >:("))

#################
#    TICKETS    #
#################


@permission_required('clubby.is_user')
def TicketsByEventList(request, event_id):
    # ha elegido la cantidad de tickets tipo que queria.
    if (request.method == 'POST'):
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event']
            category = form.cleaned_data['category']
            quantity = form.cleaned_data['quantity']
            if (quantity > 4):
                quantity = 4  # max you can purchase

            logged = request.user
            event = Event.objects.filter(pk=event_id)[0]
            num_tickets_user_event = Ticket.objects.filter(
                event=event).filter(user=logged).count()

            max_purchasable = 4 - num_tickets_user_event
            max_tickets = False
            if(quantity > max_purchasable):
                max_tickets = True
                quantity = max_purchasable

            missing_tickets = False
            miss = 0
            user_is_broke = False
            if(not max_tickets):
                tickets_from_db = Ticket.objects.filter(
                    event=event).filter(user=None).filter(category=category)
                to_buy = len(tickets_from_db) if (
                    len(tickets_from_db) <= quantity) else quantity

                print(str(to_buy) + str(tickets_from_db))

                total_cost = tickets_from_db[0].price * to_buy
                if (total_cost > logged.profile.funds):
                    user_is_broke = True

                else:
                    logged.profile.funds -= total_cost
                    logged.profile.save()

                    owner = event.club.owner
                    # we take the 5% off the purchase.
                    owner.profile.funds += total_cost - \
                        total_cost*Decimal("0.05")
                    owner.save()

                    for x in range(to_buy):
                        tick = tickets_from_db[x]
                        tick.user = logged
                        tick.save()
                        tick.refresh_from_db()

                        qr = QR_Item(is_used=False, priv_key=get_random_string(length=16), user=logged, ticket=tick,
                                     fecha=datetime.datetime.now(), expiration_date= tick.event.end_datetime)
                        qr.save()

                    event.atendees.add(request.user)
                    # event.save() no need to save as add saves it for us.
                    return HttpResponseRedirect(reverse('purchase-confirm'))

            context = {'event': event, 'missing_tickets': missing_tickets,
                'miss': miss, 'max_tickets': max_tickets, 'user_is_broke': user_is_broke}
            return render(request, 'clubby/event/detail.html', context)

    else:
        event = Event.objects.filter(pk=event_id)[0]
        tickets_from_db = Ticket.objects.filter(event=event).filter(user=None)
        tickets_from_db = Ticket.objects.filter(event=event).filter(user=None)

        categories = []
        tickets = []
        for t in tickets_from_db:
            if (t.category not in categories):
                categories.append(t.category)
                tickets.append(t)

        ticket_ammount = dict()
        for t in range(len(tickets)):

            # collect number of owned items
            tickets[t].owned = Ticket.objects.filter(event=event).filter(user=request.user).count()

            # returns the ammount of unsold tickets for an event and category
            form = TicketPurchaseForm(
                initial={'event': event.pk, 'category': categories[t]})
            ticket_ammount[tickets[t]] = form

        context = {'ticket_ammount': ticket_ammount}
        return render(request, 'clubby/ticket/list.html', context)

###############
#    FUNDS    #
###############
@login_required
def add_funds(request, ammount):
    form = FundsForm()
    form.initial['ammount'] = float(ammount) * 100.0
    form.fields['ammount'].widget = forms.HiddenInput()
    return render(request, 'clubby/funds.html', {'form': form, 'key': settings.STRIPE_PUBLISHABLE_KEY, 'ammount': ammount})


@login_required
def clean_charge(request):
    return render(request,'clubby/charge.html')


@login_required
def charge(request, ammount):  # new
    if request.method == 'POST':
        form = FundsForm(request.POST)
        quantity = form['ammount'].value()

        charge = stripe.Charge.create(
        amount=int(quantity),
        currency='eur',
        description='Money spent at Clubby',
        source=request.POST['stripeToken']
    )

        profile = request.user.profile
        profile.funds += Decimal(str(float(quantity)/100))
        profile.save()

        return render(request,'clubby/charge.html')


###############
#   PAYOUTS   #
###############

@permission_required('clubby.is_owner')
def register_stripe_account(request):
    code, error , error_description = None, None, None

    try:
        code = request.GET['code']
    except:
        error = request.GET['error']
        error_description = request.GET['error_description']
        print(error)
        print(error_description)

    if(error != None):
        return render(request,'clubby/error.html',{'error':str(error) + ", "+str(error_description)})
        
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code,)
    except stripe.oauth_error.OAuthError as e:
        return render(request,'clubby/error.html',{"error": "Invalid authorization code: " + code})
    except Exception as e:
        return render(request,'clubby/error.html',{"error": "An unknown error occurred."})

    connected_account_id = response["stripe_user_id"]

    profile = request.user.profile
    profile.stripe_account_id = connected_account_id
    profile.save()

    return render(request,'clubby/charge.html')

@permission_required('clubby.is_owner')
def payout(request): # new

    #this are testing bank accounts from all over the world.
    # posible_destinations = ['ES0700120345030000067890','AT611904300234573201','BE62510007547061','DK5000400440116243','EE382200221020145689',
    # 'FI2112345600000785','FR1420041010050500013M02606','DE89370400440532013000','IE29AIBK93115212345678','IT40S0542811101000000123456',
    # 'LT121000011101001000','LU280019400644750000','NL39RABO0300065264','NO9386011117947','PT50000201231234567890154','SE8150000000058398257400','GB82WEST12345698765432']
    
    user = request.user
    profile = user.profile
    try:
        club = Club.objects.filter(owner=user)[0]
    except:
        club = ''

    #     form = FundsForm()
    
    if request.method == 'POST':
        form = FundsForm(request.POST)
        quantity = form['ammount'].value()
        quantity = float(quantity)
        funds = float(profile.funds)
        print(quantity) #<-- actual number

        if(quantity > funds):
            context = {'logged_user': user,'user_profile': profile, 'club':club, 'form':form, 'limited_funds':True}
            return render(request,'clubby/profile.html',context)
        else:
            quantity = int(quantity*100)

            session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'name': "Clubby",
                'amount': str(quantity),
                'currency': 'eur',
                'quantity': 1,
            }],
            payment_intent_data={
                'application_fee_amount': int(quantity*0.05),
                'transfer_data': {
                'destination': profile.stripe_account_id,
                },
            },
            success_url='https://clubby-sprint3.herokuapp.com/',
            cancel_url='https://clubby-sprint3.herokuapp.com/clubby/profile',
            )
            
            profile = request.user.profile
            profile.funds -= Decimal(str(float(quantity/100)))
            profile.save()

            return render(request,'clubby/charge.html')
    else:
        raise PermissionDenied(_("Incorrect accesing to resource."))

#################
#    PREMIUM    #
#################
@permission_required('clubby.is_owner')
def get_premium(request):  # new
    if request.method == 'POST':
        form = PremiumForm(request.POST)
        has_accepted = form['accept'].value()
        if(has_accepted):
            owner = request.user

            if(owner.profile.funds < Decimal("15")):
                return render(request, 'clubby/premium.html', {'form': form, 'not_enough_funds': True})
            else:
                # These are models created by the django-background-tasks package...
                owner_tasks = Task.objects.filter(creator_object_id=owner.pk)
                profile = owner.profile

                print(owner_tasks)

                if(len(owner_tasks) == 0):
                    profile.renew_premium = True
                    profile.funds -= Decimal("15")
                    my_group = Group.objects.get(name='premium owner')
                    my_group.user_set.add(owner)
                    owner.save()
                    profile.save()
                    now = datetime.datetime.now()
                    if(now.month == 12):
                        next_payment = datetime.datetime(now.year+1, 1, 2, 2)
                    else:
                        next_payment = datetime.datetime(
                            now.year, now.month + 1, 2, 2)

                    # check_premium(owner.pk, schedule=next_payment, creator=owner) #Solo la crearemos una vez.
                    # 10 Minutos como testing.
                    check_premium(owner.pk, schedule=600, creator=owner)
                else:
                    profile.funds -= Decimal("15")
                    profile.renew_premium = True
                    my_group = Group.objects.get(name='premium owner')
                    my_group.user_set.add(owner)
                    profile.save()

                #check_premium(owner.pk, schedule=60)
                return render(request, 'clubby/charge.html')
        else:
            return render(request, 'clubby/premium.html', {'form': form, 'not_accepted': True})
    else:
        form = PremiumForm(initial={'accept': False})
        return render(request, 'clubby/premium.html', {'form': form})


@permission_required('clubby.is_premium_owner')
def cancel_premium(request):
    if request.method == 'POST':
        form = PremiumForm(request.POST)
        has_accepted = form['accept'].value()
        if(has_accepted):
            owner = request.user
            profile = owner.profile
            profile.renew_premium = False
            my_group = Group.objects.get(name='premium owner')
            my_group.user_set.remove(owner)
            profile.save()
            return render(request, 'clubby/charge.html')
        else:
            return render(request, 'clubby/cancel_premium.html', {'form': form, 'not_accepted': True})
    else:
        form = PremiumForm(initial={'accept': False})
        return render(request, 'clubby/cancel_premium.html', {'form': form})

########################
#    EDIT USER DATA    #
########################


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request=request)
        if (form.is_valid()):
            user = request.user
            profile = user.profile
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')

            user.save()

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            profile.bio = form.cleaned_data.get('bio')
            profile.location = form.cleaned_data.get('location')
            profile.picture = form.cleaned_data.get('picture')

            profile.save()
            return redirect('profile')
        else:
            return render(request, 'clubby/edit_profile.html', {'form': form})
    else:
        user = request.user
        form = EditProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,'bio': user.profile.bio,
                                'location': user.profile.location, 'picture': user.profile.picture,'birth_date': user.profile.birth_date})
        return render(request, 'clubby/edit_profile.html', {'form': form})

##################
#   STATISTICS   #
##################

@permission_required('clubby.is_premium_owner')
def get_stats(request):
    # PRODUCTOS VENDIDOS TOTAL
    products_by_club = Product.objects.filter(club=request.user.club)
    product_ammounts = []
    products = []
    for product in products_by_club:
        products.append(str(product.name))
        product_ammounts.append(
            QR_Item.objects.filter(product=product).count())

    context = {'product_labels': json.dumps(
        products), 'product_data': json.dumps(product_ammounts)}

    # ENTRADAS VENDIDAS POR EVENTO
    events_by_club = Event.objects.filter(club=request.user.club)
    events = []
    event_ammounts = []
    for event in events_by_club:
        events.append(str(event))
        tickets_for_event = Ticket.objects.filter(event=event)
        cont = 0
        for ticket in tickets_for_event:
            cont += QR_Item.objects.filter(ticket=ticket).count()
        event_ammounts.append(cont)

    context['event_labels'] = json.dumps(events)
    context['event_data'] = json.dumps(event_ammounts)

    # DINERO GENERADO TOTAL AÑO(SUMA ACUMULADA)
    cont = 0
    now = datetime.datetime.now().date()

    context['month_labels'] = json.dumps(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    sales_month_products = []
    sales_month_events = []
    cumsum_products = 0
    cumsum_events = 0

    from calendar import monthrange
    for month in range(1, 13):
        first = now.replace(month=month, day=1)
        last = now.replace(month=month, day=monthrange(now.year, month)[1])

        products_by_club = Product.objects.filter(club=request.user.club)

        for product in products_by_club:
            cumsum_products += QR_Item.objects.filter(product=product).filter(fecha__gte=first).filter(fecha__lte=last).count()*product.price

        events_by_club = Event.objects.filter(club=request.user.club).filter(start_date__gte=first).filter(start_date__lte=last)

        for event in events_by_club:
            tickets_for_event = Ticket.objects.filter(event=event)

            for ticket in tickets_for_event:
                cumsum_events += QR_Item.objects.filter(ticket=ticket).count()*ticket.price

        sales_month_products.append(str(cumsum_products))
        sales_month_events.append(str(cumsum_events))

    context['sales_month_products'] = sales_month_products
    context['sales_month_events'] = sales_month_events

    #MEDIA DE LAS VALORACIONES DEL CLUB POR MES.
    
    rating_average = []

    for month in range(1, 13):
        first = now.replace(month=month, day=1)
        last = now.replace(month=month, day=monthrange(now.year, month)[1])
        ratings_by_club_date = Rating.objects.filter(club=request.user.club).filter(fecha__gte=first).filter(fecha__lte=last)
        starcount = 0
        cumsum = 0
        for r in ratings_by_club_date:
            cumsum += r.stars
            starcount += 1

        if(starcount != 0):
            rating_average.append(cumsum/starcount)
        else:
            rating_average.append(0.0)

    context['rating_average'] = json.dumps(rating_average)

    return render(request, 'clubby/charts/statistics.html', context)




###############
#   SPOTIFY   #
###############
@permission_required('clubby.is_user')
def connect_spotify(request):
    code, error = None, None
    try:
        code = request.GET.get("code")
        print('code: '+ code)
    except:
        print('no code found')

    try:
        error = request.GET.get("error")
        print('error: '+ error)
    except:
        print('no error found')

    if(code != None):
        token_uri = 'https://accounts.spotify.com/api/token'

        redirect_uri = 'https://clubby-sprint3.herokuapp.com/clubby/spotify/authorize/'
        client_id ='7af4e7e36a454ec09746fa13559947d9'
        client_secret = '77803dff87ba476fb8ccdaf0750d695a'

        data = {'grant_type':'authorization_code',
        'code':code, 
        'redirect_uri':redirect_uri,
        'client_id':client_id,
        'client_secret':client_secret} 

        response = requests.post(url=token_uri,data=data)
        data = json.loads(response.text)  

        spotify_expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])

        spotify_access_token = data['access_token']
        spotify_refresh_token = data['refresh_token']
        profile = request.user.profile
        profile.spotify_access_token = spotify_access_token
        profile.spotify_refresh_token = spotify_refresh_token
        profile.spotify_expiration_date = spotify_expiration_date
        profile.save()
    else:
        print(error)

    return redirect('profile')

@permission_required('clubby.is_user')
def view_recommended_events(request):
    profile = request.user.profile
    now_date = pytz.utc.localize(datetime.datetime.now())
    if(profile.spotify_expiration_date > now_date):
        print('pedimos un nuevo token')
        token_uri = 'https://accounts.spotify.com/api/token'

        client_id ='7af4e7e36a454ec09746fa13559947d9'
        client_secret = '77803dff87ba476fb8ccdaf0750d695a'

        data = {'grant_type':'refresh_token',
        'refresh_token':profile.spotify_refresh_token,
        'client_id':client_id,
        'client_secret':client_secret} 

        response = requests.post(url=token_uri,data=data)
        data = json.loads(response.text)

        spotify_expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
        spotify_access_token = data['access_token']

        profile.spotify_access_token = spotify_access_token
        profile.spotify_expiration_date = spotify_expiration_date
        profile.save()
    else:
        spotify_access_token = profile.spotify_access_token

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + spotify_access_token,
    }

    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers = headers, timeout = 5)

    data = json.loads(response.text)  

    genres = ['rock', 'pop','techno','electro','hip hop', 'trap','reggaeton','indie','metal', 'latin',
        'edm','cumbia','rap','house','r&b','latino','dance','k-pop','funk','folk','disco','emo','flamenco',
        'country','trance','reggae','salsa','soul','jazz','ska','dubstep','rumba','punk','ranchera','grunge']

    genres_count = {'rock':0, 'pop':0,'techno':0,'electro':0,'hip hop':0, 'trap':0,'reggaeton':0,'indie':0,'metal':0, 'latin':0,
        'edm':0,'cumbia':0,'rap':0,'house':0,'r&b':0,'latino':0,'dance':0,'k-pop':0,'funk':0,'folk':0,'disco':0,'emo':0,'flamenco':0,
        'country':0,'trance':0,'reggae':0,'salsa':0,'soul':0,'jazz':0,'ska':0,'dubstep':0,'rumba':0,'punk':0,'ranchera':0,'grunge':0}

    try:
        for d in data['items']:
            for g in d['genres']:
                for genre in genres:
                    if(genre in g):
                        genres_count[genre] = 1
    except:
        print('no artists found for this spotify account.')
        redirect('events')
    
    user_genres = []
    for g in genres:
        if(genres_count[g] == 1):
            user_genres.append(g)

    print(user_genres)

    query = Q()
    for g in user_genres:
        query = query | Q(event_type=g)

    start = datetime.datetime.now().date()
    end = (datetime.datetime.now()+datetime.timedelta(days = 30))
    events = Event.objects.filter(start_date__gte=start).filter(start_date__lte=end).filter(query).order_by('start_date', 'start_time')
    
    context = {'object_list':events}

    return render(request,'clubby/event/list.html', context)
