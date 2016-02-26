from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IMPFCS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', lambda request: HttpResponseRedirect(reverse('frontend:foyer'))),
    url(r'^site/', include('frontend.urls', namespace='frontend')),
#    url(r'^ccc/',views.ccc),
)
