from django.conf.urls import patterns, url
from dissertations import views

urlpatterns = patterns('',
                       # ex /dissertations/download/
                       url(r'^download/$', views.DissertationIndexView.as_view(), name='download'),
                       # ex /meetings/2013/
                       #url(r'^(?P<year>\d{4})/$', views.MeetingsDetailView.as_view(), name='meeting_detail'),
                       # ex /meetings/abstract/add/
                       #url(r'^abstract/add/$', views.AbstractCreateView1.as_view(), name='create_abstract'),
                       #url(r'^abstract/add/$', 'meetings.views.create_abstract', name='create_abstract'),
                       # ex /meetings/abstract/thanks/
                       #url(r'^abstract/thanks/$', views.AbstractThanksView.as_view(), name='thanks'),

                       )
