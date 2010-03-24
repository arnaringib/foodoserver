from django.shortcuts import render_to_response, get_object_or_404

from foodo.restaurants.models import Restaurant

def index(request):
    return render_to_response('mobile/index.html')
    
    
def detail(request, restaurant_id): 
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render_to_response('mobile/details.html', {'restaurant': restaurant})