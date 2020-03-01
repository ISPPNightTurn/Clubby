from django.urls import path, include
from . import views

# we might wanna test this later on, this changes the views from custom written to django generic.
# https://docs.djangoproject.com/en/3.0/intro/tutorial04/#amend-urlconf

app_name = 'clubby' #<-- this makes identifying the urls as clubby:urlname
#This is here as an example:
urlpatterns = [
    # ex: /clubby/polls
    path('polls', views.index, name='polls-index'),
    # ex: /clubby/polls/5/
    path('polls/<int:question_id>/', views.detail, name='polls-detail'),
    # ex: clubby/polls/5/results/
    path('polls/<int:question_id>/results/', views.results, name='polls-results'),
    # ex: /clubby/polls/5/vote/
    path('polls/<int:question_id>/vote/', views.vote, name='polls-vote'),
]

urlpatterns += [
    path('', views.landing, name='landing'),
    path('clubs', views.ClubListView.as_view(), name='clubs'),
    path('club/<int:pk>', views.ClubDetailView.as_view(), name='club-detail'),
    path('events', views.EventListView.as_view(), name='events'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
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