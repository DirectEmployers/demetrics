from django.conf.urls import patterns, include, url
from django.contrib import admin
from demetrics.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demetrics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', read_my_jobs),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', GAAuth, name='GAAuth'),
    url(r'^auth_return$', auth_return, name='auth_return'),
    url(r'^gapi$', ga_ajax, name='ga_ajax'),
)