from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db.models import Avg
from django.utils import simplejson
from datetime import datetime
import hashlib
import random

#from django.db import connection

from foodo.restaurants.models import Restaurant, Type, Review, MenuItem, User, Rating

def JsonResponse(data='', code=200, error=''): 
    response_dict = {
        'responseData': data,
        'responseCode': code,
    }
    
    if (error):
        response_dict.update({'errorMessage': error})
    
    return HttpResponse(simplejson.dumps(response_dict, indent=4, ensure_ascii=True), mimetype='application/javascript')
    
def getRestaurantsDict(restaurants):
    r_d = {
        'Restaurants': []
    }
    for r in restaurants:
        d = {
            "id": r.pk,
            "website": r.website,
            "city": r.city,
            "name": r.name,
            "zip": r.zip,
            "created": str(r.created),
            "pricegroup": r.pricegroup.pk,
            "phone": r.phone,
            "address": r.address,
            "lat": r.lat,
            "lng": r.lng,
            "email": r.email,
            "types": [],
            "description": r.description,
        }
        if (r.avg_rating):
            d['rating'] = "%.1f" % r.avg_rating
        else:
            d['rating'] = 0
        
        for t in r.types.all():
            d['types'].append(t.id)
        
        r_d['Restaurants'].append(d)
    return r_d

def getUserDict(user):
    return {'User': {'email': user.email, 'apikey': user.apikey}}

def index(request):
    restaurants = Restaurant.objects.annotate(avg_rating=Avg('rating__rating')).order_by('pk')
    r_dict = getRestaurantsDict(restaurants)
    return JsonResponse(r_dict)
    
def detail(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.annotate(avg_rating=Avg('rating__rating')).get(pk=restaurant_id)
    except (KeyError, Restaurant.DoesNotExist):
        return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % restaurant_id)
    else:
        r_dict = getRestaurantsDict([restaurant,])
        return JsonResponse(r_dict)
    
def menu(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        menu = MenuItem.objects.filter(restaurant=restaurant)
    except (KeyError, Restaurant.DoesNotExist):
        return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % restaurant_id)
    else:
        d = {'Menu': []}
        for item in menu:
            d['Menu'].append({"id": item.id, "price": item.price, "name": item.name})
        return JsonResponse(d)
    
def reviews(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except (KeyError, Restaurant.DoesNotExist):
        return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % restaurant_id)
    else:
        d = {'Reviews': []}
        for review in Review.objects.filter(restaurant=restaurant):
            d['Reviews'].append({
                "id": review.id,
                "description": review.description, 
                "created": str(review.created),
                "user": "%s %s" % (review.user.firstName, review.user.lastName),
            })
        return JsonResponse(d)

def rate(request, restaurant_id, rating, apikey):
    """ add a user rating for restaurant, user is limited to one rating"""
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        user = User.objects.get(apikey=apikey)
    except (KeyError, Restaurant.DoesNotExist):
        return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % restaurant_id)
    except (KeyError, User.DoesNotExist):
        return JsonResponse(code=404, error='Bad apikey')
    else:
        if not restaurant.is_rating_valid(int(rating)):    
            return JsonResponse(code=404, error='Invalid rating')
        else:
            try:
                prev_rating = Rating.objects.get(user=user, restaurant=restaurant)
                prev_rating.rating = int(rating)
                prev_rating.save()
            except (KeyError, Rating.DoesNotExist):
                r = Rating(user=user, restaurant=restaurant, rating=int(rating))
                r.save()
            return detail(request, restaurant_id)
            #return HttpResponseRedirect(reverse('foodo.api.views.detail', args=(restaurant.id,)))

def types(request):
    d = {'Types': []}
    for t in Type.objects.all().order_by('name'):
        d['Types'].append({"id": t.id, "name": t.name,})
    return JsonResponse(d)
    
def signup(request):
    try:
        apikey = hashlib.md5("%s%s%sFoodo" % (request.GET['email'], request.GET['password'], random.randint(1000,9999))).hexdigest()
        u = User(email=request.GET['email'], password=request.GET['password'], apikey=apikey)
        if (request.GET.__contains__('firstname')):
            u.firstName = request.GET['firstname']
        if (request.GET.__contains__('lastname')):
            u.lastName = request.GET['lastname']
        u.save();
        return JsonResponse(getUserDict(u))
    except:
        return JsonResponse(code=404, error='User exists')
    
def login(request):
    try:
        user = User.objects.get(email=request.GET['email'], password=request.GET['password'])
        return JsonResponse(getUserDict(user))
    except (KeyError, User.DoesNotExist):
        return JsonResponse(code=404, error="Incorrect username/password")        
