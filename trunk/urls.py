from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^restaurants/$', 'foodoserver.restaurants.views.index'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'foodoserver.restaurants.views.detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/rate/$', 'foodoserver.restaurants.views.rate'),
    
#    (r'^api/restaurants/$', 'foodoserver.restaurants.api.index'),
#    (r'^api/restaurants/(?P<restaurant_id>\d+)/$', 'foodoserver.restaurants.api.detail'),

    (r'^admin/', include(admin.site.urls)),
    
    (r'^api/', include('foodoserver.api.urls')),
)
