from django.conf.urls import patterns, url
from members import views

urlpatterns = patterns('',
                       # ex /members/
                       url(r'^$', views.MembersIndexView.as_view(), name='members'),
                       # ex /members/23/
                       url(r'^(?P<pk>\d+)/$', views.MemberUpdateView.as_view(), name='member_update'),
                       # ex /members/update/
                       url(r'^update/$', views.MemberUpdateView.as_view(), name='member_update_root'),
                       )