from django.conf.urls import patterns, include, url
from typhoon.views import home, verification

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'typhoon.views.home', name='home'),
    # url(r'^typhoon/', include('typhoon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', home),
    url(r'^home/verify/$', verification),
)
