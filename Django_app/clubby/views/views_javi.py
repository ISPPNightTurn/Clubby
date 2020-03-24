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

from ..forms import TicketCreateModelForm, RatingCreateModelForm

from datetime import datetime, timedelta

from ..models import Club, Event, Profile, Product, Ticket, QR_Item, Rating

import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

#################
#    History    #
#################

@permission_required('clubby.is_user')
def CheckHistory(request):

    current_user = request.user

    list = QR_Item.objects.filter(user = current_user).order_by('-fecha')

    for qr_item in list:
        if qr_item.product != None:
            dn = datetime.datetime.now() - timedelta(hours=6)
            d = qr_item.fecha
            d = d.replace(tzinfo=None)
        elif qr_item.ticket != None:
            dn = datetime.datetime.now() - timedelta(hours=qr_item.ticket.event.duration)
            d = datetime.datetime(qr_item.ticket.event.start_date.year, qr_item.ticket.event.start_date.month, 
                qr_item.ticket.event.start_date.day) + timedelta(hours=qr_item.ticket.event.start_time)
        if dn > d:
            qr_item.timed_out = True
            qr_item.save()

    return render(request, 'clubby/purchase/history_list.html', {"list": list})

#################
#  Order Events #
#################

# @login_required
# def EventsByUserList(request, order = None):

#     current_user = request.user

#     if order is None or order is 1:

#         list = Event.objects.filter(atendees = current_user).order_by('start_date' , 'start_time')

#         aux = Event.objects.none()

#         for event in list:
#             dn = datetime.datetime.now() - timedelta(hours=event.duration)
#             d = datetime.datetime(event.start_date.year, event.start_date.month, 
#                 event.start_date.day) + timedelta(hours=event.start_time)
#             if dn > d:
#                 aux |= Event.objects.filter(pk = event.pk)
#                 list = list.exclude(pk = event.pk)

#     return render(request, 'clubby/event/list.html', {"object_list": list, "old_object_list": aux})

# @login_required
# def EventList(request, order = None):

#     if order is None or order is 1:

#         list = Event.objects.filter(start_date__gte = datetime.datetime.now().date()).order_by('start_date' , 'start_time')

#         for event in list:
#             dn = datetime.datetime.now() - timedelta(hours=event.duration)
#             d = datetime.datetime(event.start_date.year, event.start_date.month, 
#                 event.start_date.day) + timedelta(hours=event.start_time)
#             if dn > d:
#                 list = list.exclude(pk = event.pk)


#     return render(request, 'clubby/event/list.html', {"object_list": list})

# @permission_required('clubby.is_owner')
# def EventsByClubAndFutureList(request, order = None):

#     club = Club.objects.filter(owner = request.user)[0]

#     if order is None or order is 1:

#         list = Event.objects.filter(start_date__gte = datetime.datetime.now().date()).filter(club = club).order_by('start_date' , 'start_time')

#         aux = Event.objects.none()

#         for event in list:
#             dn = datetime.datetime.now() - timedelta(hours=event.duration)
#             d = datetime.datetime(event.start_date.year, event.start_date.month, 
#                 event.start_date.day) + timedelta(hours=event.start_time)
#             if dn > d:
#                 aux |= Event.objects.filter(pk = event.pk)
#                 list = list.exclude(pk = event.pk)


#     return render(request, 'clubby/event/list.html', {"object_list": list, "old_object_list": aux})

#################
#     Rating    #
#################

@login_required
def ClubListRating(request, club_id, order = None):

    page = request.GET.get('page', 1)
    
    if order is None or order is 1:
        order = 1
        list = Rating.objects.filter(club_id = club_id).exclude(user_id=request.user.id).order_by('-fecha')
        listU = Rating.objects.filter(club_id = club_id,user_id=request.user.id)
        paginator = Paginator(list, 5)

    if order is 2:
        list = Rating.objects.filter(club_id = club_id).exclude(user_id=request.user.id).order_by('-stars','-fecha')
        listU = Rating.objects.filter(club_id = club_id,user_id=request.user.id)
        paginator = Paginator(list, 5)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    return render(request, 'clubby/club/rating_list.html', {"list": list,"listU":listU, "club_id":club_id, "order":order})

@permission_required('clubby.is_user')
def ClubCreateRating(request, club_id):

    if (request.method == 'POST'):
        form = RatingCreateModelForm(data=request.POST or None)
        if form.is_valid():

            listU = Rating.objects.filter(club_id = club_id,user_id=request.user.id)
            stars = form.cleaned_data['stars']
            text = form.cleaned_data['text']

            if len(listU) is 0 :             
                t = Rating(stars=stars, text=text,fecha=datetime.datetime.now(),
                    club_id=club_id,user_id=request.user.id)
                t.save()

            else:
                Rating.objects.filter(club_id = club_id,user_id=request.user.id).update(stars=stars, text=text,fecha=datetime.datetime.now())

            return HttpResponseRedirect(reverse('clubs'))

    else:
        form = RatingCreateModelForm(initial={'stars':10,'text':''})
        return render(request, 'clubby/club/rating_create.html', {'form': form})