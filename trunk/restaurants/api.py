from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core import serializers
from foodoserver.restaurants.models import Restaurant

def index(request):
    restaurant_list = Restaurant.objects.all().order_by('-name')
    data = serializers.serialize('json', restaurant_list)
    return HttpResponse(data)
    
def detail(request, restaurant_id):
    restaurant = list(Restaurant.objects.get(pk=restaurant_id))
    data = serializers.serialize('json', restaurant)
    return HttpResponse(data)
    