from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db.models import Avg
from django.utils import simplejson
import hashlib
import random

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
        d = {"pk": r.pk, "fields": {
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
        }}
        if (r.rating__rating__avg):
            d['fields']['rating'] = r.rating__rating__avg
        else:
            d['fields']['rating'] = 0
        
        for t in r.types.all():
            d['fields']['types'].append(t.id)
        
        r_d['Restaurants'].append(d)
    return r_d

def index(request):
    restaurants = Restaurant.objects.annotate(Avg('rating__rating')).order_by('pk')
    r_dict = getRestaurantsDict(restaurants)
    return JsonResponse(r_dict)
    
def detail(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.annotate(Avg('rating__rating')).get(pk=restaurant_id)
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
            d['Menu'].append({"pk": item.id, "fields": {"price": item.price, "name": item.name}})
        return JsonResponse(d)
    
#TODO use JsonResponse 
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
    
    
    
    
