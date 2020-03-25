from django.urls import path, include
from . import views
from django.conf.urls import url

from django.conf import settings
from django.contrib.auth import logout



# we might wanna test this later on, this changes the views from custom written to django generic.
# https://docs.djangoproject.com/en/3.0/intro/tutorial04/#amend-urlconf

#app_name = 'clubby' #<-- this makes identifying the urls as clubby:urlname but its useless for us.
#This is here as an example:
# urlpatterns = [
#     # ex: /clubby/polls
#     path('polls', views.index, name='polls-index'),
#     # ex: /clubby/polls/5/
#     path('polls/<int:question_id>/', views.detail, name='polls-detail'),
#     # ex: clubby/polls/5/results/
#     path('polls/<int:question_id>/results/', views.results, name='polls-results'),
#     # ex: /clubby/polls/5/vote/
#     path('polls/<int:question_id>/vote/', views.vote, name='polls-vote'),
# ]

urlpatterns = [
    path('', views.landing, name='landing'),
    path('clubs', views.ClubListView.as_view(), name='clubs'),
    path('club/<int:pk>', views.ClubDetailView.as_view(), name='club-detail'),
    path('events', views.EventListView.as_view(), name='events'),
    path('events/<int:order>', views.EventList, name='events'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('myevents', views.EventsByUserList, name='my-events'),
    path('myevents/<int:order>', views.EventsByUserList, name='my-events'),
    # path('mypublishedevents', views.EventsByClubListView.as_view(), name='my-published-events'),
    path('mypublishedeventsfuture', views.EventsByClubAndFutureList, name='my-events-future'),
    path('mypublishedeventsfuture/<int:order>', views.EventsByClubAndFutureList, name='my-events-future'),
    path('event/create', views.EventCreateView.as_view(), name='event-create'),
    path('profile', views.profile, name='profile'),
]

urlpatterns += [
    url('signup/user', views.signup_user, name='signup-user'),
    url('signup/owner', views.signup_owner, name='signup-owner'),
]

urlpatterns += [  
    path('club/create/', views.ClubCreate.as_view(), name='club-create'),
    path('club/<int:pk>/update/', views.ClubUpdate.as_view(), name='club-update'),
    path('club/<int:pk>/delete/', views.ClubDelete.as_view(), name='club-delete'),
]

urlpatterns += [  
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/update/', views.ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product-delete'),
    path('product/list/<int:club_id>', views.ProductsByClubList, name='product-list'),
    path('myproducts', views.ProductsByClubListView.as_view(), name='my-products'),
]

urlpatterns += [  
    path('ticket/list/<int:event_id>', views.TicketsByEventList, name='ticket-list'),
]

urlpatterns += [
    path('addFunds/<int:ammount>', views.add_funds, name='add-funds'),
    path('charge/<int:ammount>', views.charge, name='charge'),
    path('getPremium', views.get_premium, name='get-premium'),
    path('cancelPremium', views.cancel_premium, name='cancel-premium'), 
]

urlpatterns += [
    path('event/<int:event_id>/create_tickets', views.EventCreateTickets, name='create-tickets'),
    path('club/<int:club_id>/rating_list', views.ClubListRating, name='list-rating'),
    path('club/<int:club_id>/rating_list/<int:order>', views.ClubListRating, name='list-rating'),
    path('club/<int:club_id>/rating_create', views.ClubCreateRating, name='create-rating'),
]

urlpatterns += [  
    path('purchase/list/', views.QRsByUserListView.as_view(), name='my-purchases'),
    path('history/list/', views.CheckHistory, name='my-history'),
    path('purchase/<int:qr_item_id>/<slug:priv_key>', views.DisplayQRItemView, name='purchase-display'),   
]


# urlpatterns += [   
#     path('event/create', views.add_event, name='add-event'),
# ]


# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('social/success/', views.socialsuccess, name="social-sucess"),
]

urlpatterns += [
    url(r'^api/chart/data/$', views.ChartData.as_view()),
]



'''
This is a local page for the clubby project where all URLS will be defined. You can see some examples below.

https://docs.djangoproject.com/en/3.0/ref/urls/  full list of view methods

examples:
path(route, view, kwargs=None, name=None)
urlpatterns = [
    path('index/', views.index, name='main-view'),
    path('bio/<username>/', views.bio, name='bio'),
    path('articles/<slug:title>/', views.article, name='article-detail'),
    path('articles/<slug:title>/<int:section>/', views.section, name='article-section'),
    path('weblog/', include('blog.urls')),
    ...
]

re_path(route, view, kwargs=None, name=None)
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^weblog/', include('blog.urls')),
    ...
]

'''