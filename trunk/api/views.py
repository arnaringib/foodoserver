# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
import hashlib
import random

from foodoserver.restaurants.models import Restaurant, Type, Review, MenuItem, User, Rating

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
    
def rate(request, restaurant_id, rating, apikey):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    user = get_object_or_404(User, apikey=apikey)
    
    if restaurant.is_rating_valid(int(rating)):
        r = Rating(user=user, restaurant=restaurant, rating=int(rating))
        r.save()
        return HttpResponseRedirect(reverse('foodoserver.api.views.detail', args=(restaurant.id,)))
    else:
        return HttpResponse("Invalid rating: %s" % rating)

def types(request):
    data = serializers.serialize("json", Type.objects.all().order_by('name'))
    return HttpResponse(data)

def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    data = serializers.serialize("json", MenuItem.objects.filter(restaurant=restaurant))
    return HttpResponse(data)

def signup(request):
    try:
        existing_user = User.objects.get(email=request.GET['email'])
    except (KeyError, User.DoesNotExist):
        apikey = hashlib.md5("%s%s%sFoodo" % (request.GET['email'], request.GET['password'], random.randint(1000,9999))).hexdigest()
        u = User(email=request.GET['email'], password=request.GET['password'], apikey=apikey)
        if (request.GET.__contains__('firstname')):
            u.firstName = request.GET['firstname']
        if (request.GET.__contains__('lastname')):
            u.lastName = request.GET['lastname']
        u.save();
        return HttpResponse(serializers.serialize("json", [u,]))
    else:
        return HttpResponse("User exists")
    
def login(request):
    try:
        user = User.objects.get(email=request.GET['email'])
    except (KeyError, User.DoesNotExist):
        return HttpResponse("Wrong username/password")
    else:
        if (user.password == request.GET['password']):
            data = serializers.serialize("json", [user,], fields=('email','apikey'))
            return HttpResponse(data)
        else:
            return HttpResponse("Wrong username/password")
    
    
    
    