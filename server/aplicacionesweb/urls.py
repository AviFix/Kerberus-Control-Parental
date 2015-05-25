from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^inicio/(?P<protegido>\d+)?','inicio.views.inicio'),
    (r'^hello/$','inicio.views.hello'),
    (r'^sitioDenegado/$','inicio.views.sitioDenegado'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^search/$', 'books.views.search'),
)
