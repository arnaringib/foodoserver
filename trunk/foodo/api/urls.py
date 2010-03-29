from django.conf.urls.defaults import *

urlpatterns = patterns('foodo.api.views',
    (r'^restaurants/$', 'index'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
    (r'^restaurants/(?P<restaurant_id>\d+)/reviews/$', 'reviews'),
    (r'^restaurants/(?P<restaurant_id>\d+)/reviews/create/(?P<apikey>\w+)/$', 'create_review'),
    (r'^restaurants/(?P<restaurant_id>\d+)/menu/$', 'menu'),
    (r'^restaurants/(?P<restaurant_id>\d+)/rate/(?P<rating>\d+)/(?P<apikey>\w+)/$', 'rate'),
    (r'^types/$', 'types'),
    (r'^users/signup/$', 'signup'),
    (r'^users/login/$', 'login'),
    (r'^users/edit/userinfo/$', 'edit'),
    (r'^users/edit/password/$', 'editpassword'),
    (r'^users/orders/(?P<apikey>\w+)/$', 'userorders'),
    (r'^users/reviews/(?P<apikey>\w+)/$', 'userreviews'),
    (r'^order/$', 'order'),
)
