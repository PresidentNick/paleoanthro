from django.conf.urls import patterns, url
from journal import views


urlpatterns = patterns('',
                       # ex /journal/
                       url(r'^$', views.JournalHome.as_view(), name='journal'),
                       # ex /journal/content/PA2012001.jpg/
                       url(r'^content/(?P<resource>[A-Za-z0-9_\.]+)/$', views.static_redirect, name='static_content'),
                       # ex /journal/current/
                       url(r'^current/$', views.journal_current, name='current'),
                       # ex /journal/volumes/
                       url(r'^volumes/$', views.JournalIndex.as_view(), name='journal_index'),
                       # ex /journal/volumes/2013/
                       url(r'^volumes/(?P<year>\d{4})/$', views.JournalVolumes.as_view(), name='volumes'),
                       # ex /journal/volumes/2013/223/citation/
                       url(r'^volumes/(?P<year>\d{4})/(?P<content_id>\d+)/citation/$',views.journal_citation, name='citation'),
                       # ex /journal/volumes/2013/223/journal_bibtex/
                       url(r'^volumes/(?P<year>\d{4})/(?P<content_id>\d+)/bibtex/$',views.journal_bibtex, name='bibtex'),
                       # ex /journal/volumes/2013/223/ris/
                       url(r'^volumes/(?P<year>\d{4})/(?P<content_id>\d+)/ris/$', views.journal_ris, name='ris'),
                       )