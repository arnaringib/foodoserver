# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers

from foodoserver.restaurants.models import Restaurant, Type, Review

def index(request):
    data = serializers.serialize("json", Restaurant.objects.all().order_by('pk'));
    return HttpResponse(data)
    
def detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    data = serializers.serialize("json", [restaurant,])
    return HttpResponse(data)
    
def reviews(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    data = serializers.serialize("json", Review.objects.filter(restaurant=restaurant))
    return HttpResponse(data)

def types(request):
    data = serializers.serialize("json", Type.objects.all().order_by('name'))
    return HttpResponse(data)