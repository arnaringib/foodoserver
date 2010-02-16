from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core import serializers
from foodo.restaurants.models import Restaurant

def index(request):
    restaurant_list = Restaurant.objects.all().order_by('-name')
    return HttpResponse("test")
    return render_to_response('restaurants/index.html', {'restaurant_list': restaurant_list}, 
                                context_instance=RequestContext(request))

def detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render_to_response('restaurants/detail.html', {'restaurant': restaurant})

def rate(request, restaurant_id):
    r = get_object_or_404(Restaurant, pk=restaurant_id)
    if int(request.POST['rating']) in range(1,6):
        # Update rating here
        print("Ratings is: %s" % request.POST['rating'])
        return HttpResponseRedirect(reverse('foodoserver.restaurants.views.detail', args=(r.id,)))
    else:
        return render_to_response('restaurants/detail.html', {
            'restaurant': r,
            'error_message': "Invalid rating",
        }, context_instance=RequestContext(request))
    
    