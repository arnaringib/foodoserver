from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db.models import Avg
import hashlib
import random

from foodo.restaurants.models import Restaurant, Type, Review, MenuItem, User, Rating

def index(request):
    data = serializers.serialize("json", Restaurant.objects.annotate(Avg('rating__rating')).order_by('pk'), indent=4)
    # We need a better serializer to include the rating annotation
    return HttpResponse("{Restaurants: %s }" % data)
    
def detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    data = serializers.serialize("json", [restaurant,])
    return HttpResponse("{Restaurant: %s}" % data)
    
def reviews(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    data = serializers.serialize("json", Review.objects.filter(restaurant=restaurant))
    return HttpResponse("{Reviews: %s}" % data)
    
def rate(request, restaurant_id, rating, apikey):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    user = get_object_or_404(User, apikey=apikey)
    
    if restaurant.is_rating_valid(int(rating)):
        r = Rating(user=user, restaurant=restaurant, rating=int(rating))
        r.save()
        return HttpResponseRedirect(reverse('foodo.api.views.detail', args=(restaurant.id,)))
    else:
        return HttpResponse("Invalid rating: %s" % rating)

def types(request):
    data = serializers.serialize("json", Type.objects.all().order_by('name'))
    return HttpResponse("{Types: %s }" % data)

def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    data = serializers.serialize("json", MenuItem.objects.filter(restaurant=restaurant))
    return HttpResponse("{Menu: %s}" % data)

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
        data = serializers.serialize("json", [u,], fields=('email','apikey'))
        return HttpResponse(data)
    else:
        return HttpResponse("{Error: \"User exists\"}")
    
def login(request):
    try:
        user = User.objects.get(email=request.GET['email'])
    except (KeyError, User.DoesNotExist):
        return HttpResponse("{Error: \"Wrong username/password\"")
    else:
        if (user.password == request.GET['password']):
            data = serializers.serialize("json", [user,], fields=('email','apikey'))
            return HttpResponse(data)
        else:
            return HttpResponse("{Error: \"Wrong username/password\"")
    
    
    
    
