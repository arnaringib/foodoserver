from django.conf.urls.defaults import *

urlpatterns = patterns('foodo.mobile.views',
    (r'^$', 'index'),
    (r'^restaurants/(?P<restaurant_id>\d+)/$', 'detail'),
)