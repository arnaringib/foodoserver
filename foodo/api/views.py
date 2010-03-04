from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.utils import simplejson
import datetime
import hashlib
import random

from foodo.restaurants.models import Restaurant, Type, Review, MenuItem, User, Rating, Order, OrderLine

def JsonResponse(data='', code=200, error=''): 
    response_dict = {
        'responseData': data,
        'responseCode': code,
    }

    if (error):
        response_dict.update({'errorMessage': error})

    result = simplejson.dumps(response_dict, indent=4, ensure_ascii=True)
    
    if (code == 200):
        return HttpResponse(result, mimetype='application/javascript')
    elif (code == 403):
        return HttpResponseForbidden(result, mimetype='application/javascript')
    else:
        return HttpResponseNotFound(result, mimetype='application/javascript')
    
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
        
        if (r.count_rating):
            d['rating_count'] = r.count_rating
        else:
            d['rating_count'] = 0
        
            
        for t in r.types.all():
            d['types'].append(t.id)
        
        r_d['Restaurants'].append(d)
    return r_d

def getUserDict(user):
    return {'User': {'email': user.email, 'apikey': user.apikey, 'firstName': user.firstName, 'lastName': user.lastName, }}

def getReviewDict(reviews):
    d = {'Reviews': []}
    for review in reviews:
        d['Reviews'].append({
            "id": review.id,
            "description": review.description, 
            "created": str(review.created),
            "user": "%s %s" % (review.user.firstName, review.user.lastName),
        })
    return d
    
def getOrderDict(order):
    d = {'Order': {'id': order.pk, 'user': order.user.lastName}}
    return d
    
def createOrderMessage(order):
    m = '''
Order number: \t %d
Date: \t %s 
User: %s
------------------------
Item \t Price
''' % (order.id, order.created, "%s %s (%s)" % (order.user.firstName, order.user.lastName, order.user.email))
    
    s = 0
    for line in order.orderline_set.all():
        m += "%d x %s \t %d \n" % (line.count, line.item.name, line.price*line.count)
        s += line.price*line.count
        
    m += "------------------------\nTotal: \t %d" % s
    
    return m

def index(request):
    restaurants = Restaurant.objects.annotate(avg_rating=Avg('rating__rating'), count_rating=Count('rating__rating')).order_by('pk')
    r_dict = getRestaurantsDict(restaurants)
    return JsonResponse(r_dict)
    
def detail(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.annotate(avg_rating=Avg('rating__rating'), count_rating=Count('rating__rating')).get(pk=restaurant_id)
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
        d = getReviewDict(Review.objects.filter(restaurant=restaurant))
        return JsonResponse(d)

def create_review(request, restaurant_id, apikey):
    if request.method == 'POST' and "review" in request.POST:
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            user = User.objects.get(apikey=apikey)
        except (KeyError, Restaurant.DoesNotExist):
            return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % restaurant_id)
        except (KeyError, User.DoesNotExist):
            return JsonResponse(code=403, error='Bad apikey')
        else:
            r = Review(description=request.POST['review'], created=datetime.datetime.now(), restaurant=restaurant, user=user)
            r.save()
            return reviews(request, restaurant_id)
    else:
        return JsonResponse(code=403, error='Bad request')
        

def rate(request, restaurant_id, rating, apikey):
    """ add a user rating for restaurant, user is limited to one rating"""
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        user = User.objects.get(apikey=apikey)
    except (KeyError, Restaurant.DoesNotExist):
        return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % restaurant_id)
    except (KeyError, User.DoesNotExist):
        return JsonResponse(code=403, error='Bad apikey')
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
    if request.method == 'POST' and 'email' in request.POST and 'password' in request.POST:
        try:
            apikey = hashlib.md5("%s%s%sFoodo" % (request.POST['email'], request.POST['password'], random.randint(1000,9999))).hexdigest()
            u = User(email=request.POST['email'], password=request.POST['password'], apikey=apikey)
            if ('firstname' in request.POST):
                u.firstName = request.POST['firstname']
            if ('lastname' in request.POST):
                u.lastName = request.POST['lastname']
            u.save();
            return JsonResponse(getUserDict(u))
        except:
            return JsonResponse(code=403, error='User exists')
    else:
        return JsonResponse(code=403, error='Bad request')
    
def login(request):
    if request.method == 'POST' and 'email' in request.POST and 'password' in request.POST:
        try:
            user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
            return JsonResponse(getUserDict(user))
        except (KeyError, User.DoesNotExist):
            return JsonResponse(code=403, error="Incorrect username/password")        
    else:
        return JsonResponse(code=403, error='Bad request')

def order(request):
    if request.method == 'POST':
        try:
            restaurant = Restaurant.objects.get(pk=int(request.POST['restaurant_id']))
            user = User.objects.get(apikey=request.POST['apikey'])
        except (KeyError, Restaurant.DoesNotExist):
            return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % int(request.POST['restaurant_id']))
        except (KeyError, User.DoesNotExist):
            return JsonResponse(code=403, error='Bad apikey')
        else:
            decoder = simplejson.JSONDecoder()
            order = decoder.decode(request.POST['order'])
            
            o = Order(restaurant=restaurant, user=user)
            o.save()
                        
            for item in order:
                menuitem = MenuItem.objects.get(pk=int(item['id']))
                ol = OrderLine(item=menuitem, order=o, count=int(item['amount']), price=menuitem.price)            
                ol.save()
            
            
            send_mail('Order from Foodo (#%d)' % o.pk, createOrderMessage(o), 'foodogroup@gmail.com', ['foodogroup@gmail.com'], fail_silently=False)
            
            return JsonResponse(getOrderDict(o))
    else:
        return JsonResponse(code=403, error='Bad request')
        
'''
def order(request):
    if request.method == 'POST':
        try:
            restaurant = Restaurant.objects.get(pk=int(request.POST['restaurant_id']))
            user = User.objects.get(apikey=request.POST['apikey'])
        except (KeyError, Restaurant.DoesNotExist):
            return JsonResponse(code=404, error='Restaurant does not exists: (%s)' % request.POST['restaurant_id'])
        except (KeyError, User.DoesNotExist):
            return JsonResponse(code=403, error='Bad apikey')
        else:
            # save order
            o = Order(restaurant=restaurant, user=user)
            o.save()
            
            return JsonResponse(getOrderDict(order))
    else:
        return JsonResponse(code=403, error='Bad request')
'''     