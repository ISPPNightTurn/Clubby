from django.urls import path, include
from . import views
from django.conf.urls import url

from django.conf import settings
from django.contrib.auth import logout


# we might wanna test this later on, this changes the views from custom written to django generic.
# https://docs.djangoproject.com/en/3.0/intro/tutorial04/#amend-urlconf

# app_name = 'clubby' #<-- this makes identifying the urls as clubby:urlname but its useless for us.
# This is here as an example:
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
    path('clubs/', views.ClubListView.as_view(), name='clubs'),
    url(r'clubs/near$', views.ClubListCloseByView.as_view(), name = 'clubs-near'),
    path('club/<int:pk>', views.ClubDetailView.as_view(), name='club-detail'),
    path('events', views.EventListView.as_view(), name='events'),
    path('events-recommended', views.view_recommended_events, name='events-recommended'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('myevents', views.EventsByUserListView.as_view(), name='my-events'),
    path('mypublishedeventsfuture',
         views.EventsByClubAndFutureListView.as_view(), name='my-events-future'),
    path('event/create', views.EventCreateView.as_view(), name='event-create'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
]

urlpatterns += [
    url('statistics', views.get_stats, name='get-stats'),

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
    path('product/<int:pk>', views.ProductDetailView.as_view(),name='product-detail'),
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
    path('product/<int:product_id>/update/',views.ProductUpdate, name='product-update'),
    path('product/<int:pk>/delete/',views.ProductDelete.as_view(), name='product-delete'),
    path('product/list/<int:club_id>',views.ProductsByClubList, name='product-list'),
    path('myproducts', views.ProductsByClubListView.as_view(), name='my-products'),
]

urlpatterns += [
    path('ticket/list/<int:event_id>',
         views.TicketsByEventList, name='ticket-list'),
]

urlpatterns += [
    path('addFunds/<int:ammount>', views.add_funds, name='add-funds'),
    path('charge/<int:ammount>', views.charge, name='charge'),
    path('charge', views.clean_charge, name='clean-charge'),
    url(r'^link-stripe/$', views.register_stripe_account, name='link-stripe'),
    path('payout/', views.payout, name='payout'),
    path('getPremium', views.get_premium, name='get-premium'),
    path('cancelPremium', views.cancel_premium, name='cancel-premium'),
    path('terms-and-conditions', views.terms, name='terms-and-conditions'),
    path('privacy-policy', views.privacy, name='privacy-policy'),
    path('politica-privacidad', views.privacidad, name='politica-privacidad'),
    path('terminos-condiciones', views.terminos, name='terminos-condiciones'),
    path('export-data',views.export,name='export-data'),
    path('delete-data', views.delete,name='delete-data')
]

urlpatterns += [
    path('event/<int:event_id>/create_tickets',
         views.EventCreateTickets, name='create-tickets'),
    path('club/<int:club_id>/rating_list',
         views.ClubListRating, name='list-rating'),
    path('club/<int:club_id>/rating_list/<int:order>',
         views.ClubListRating, name='list-rating'),
    path('club/<int:club_id>/rating_create',
         views.ClubCreateRating, name='create-rating'),
]

urlpatterns += [
    path('purchase/list/', views.QRsByUserListView.as_view(), name='my-purchases'),
    path('history/list/', views.CheckHistory, name='my-history'),
    path('purchase/<int:qr_item_id>/<slug:priv_key>',
         views.DisplayQRItemView, name='purchase-display'),
    path('QR/<int:qr_item_id>/<slug:priv_key>',
         views.QRItemView, name='QR-display'),
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('social/success/', views.socialsuccess, name="social-sucess"),
    url(r'spotify/authorize/$', views.connect_spotify, name="spotify-auth")
]


