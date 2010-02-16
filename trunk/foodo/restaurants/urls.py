from django.conf.urls.defaults import *

urlpatterns = patterns('foodoserver.restaurants.views',
    (r'^$', 'index'),
    (r'^(?P<restaurant_id>\d+)/$', 'detail'),
)