from django.conf.urls.defaults import *

urlpatterns = patterns('foodoserver.api.views',
    (r'^restaurants/$', 'index'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/reviews/$', 'reviews'),
    (r'^restaurants/(?P<restaurant_id>\d+)/menu/$', 'menu'),
    (r'^types/$', 'types'),
)
