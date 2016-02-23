"""Stalker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.7/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
admin.autodiscover()
from stalker_api import views

urlpatterns = patterns(
	'',
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url for generating access token

    url(r'^expand_list/$',views.expand_list ),
    # url for adding contacts.

    url( r'^friend_list/$' , views.list_ , name = 'friend_list'),
    # url for fetching list of all contacts.

    url( r'^refresh/$', views.update_info,name='refresh'), 
    # url for updating every contacts information/data.
    
    url(r'^profile/(?P<person_id>[0-9]+)/$', views.profile , name='profile'), 
    # url to view questions done by a particular contact.
    
    url( r'^delete/(?P<person_id>[0-9]+)/$' , views.delete_contact , name = 'remove_from_list'), # remove a person in the list of friends
    # url for deleting a contact

    url( r'^search_contest/(?P<site>\w+)/$', views.search_contestwise ,name='contest_peformance' ),       #shows list of all contests.
    # url to get list of all contest in either codechef/codeforces.
    # for codechef  : /search_contest/Codechef/
    # for codeforces: /search_contest/Codeforces/

    url( r'^contest_performance/(?P<site>\w+)/(?P<contest>\w+)/$',views.SearchForThisContest,name='list_for_a_contest'),    #shows everyone performance in a contest
    # url for fetching questions done by all contacts in a particular contest
    # for codechef   : /contest_performance/Codechef/contest_name
    # for codeforces : /contest_performance/Codeforces/contestId

    url(r'^refresh/(?P<person_id>[0-9]+)/$', views.update_a_person_info , name='refresh_a_person'), #to update information of a particular contacts.
    # url for updating a particular contact,provided by person_id/pk ,information/data

    url(r'^register/$', views.Registration) ,
    # url for registration of a new user    
)