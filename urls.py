from django.conf.urls import *
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^metrics$', read_my_jobs, name='read_my_jobs'),
    url(r'^metrics/login$', google_login, name='google_login'),
    url(r'^metrics/auth$', google_authenticate, name='google_authenticate'),
    )
