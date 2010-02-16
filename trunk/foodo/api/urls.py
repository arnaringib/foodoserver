from django.conf.urls.defaults import *

urlpatterns = patterns('foodo.api.views',
    (r'^restaurants/$', 'index'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/reviews/$', 'reviews'),
    (r'^restaurants/(?P<restaurant_id>\d+)/menu/$', 'menu'),
    (r'^restaurants/(?P<restaurant_id>\d+)/rate/(?P<rating>\d+)/(?P<apikey>\w+)$', 'rate'),
    (r'^types/$', 'types'),
    (r'^users/signup/$', 'signup'),
    (r'^users/login/$', 'login'),
)
