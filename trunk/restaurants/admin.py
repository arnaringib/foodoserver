from foodoserver.restaurants.models import Restaurant, Rating, Pricegroup, Type, Review, User
from django.contrib import admin

class RatingInline(admin.StackedInline):
    model = Rating
    extra = 1
    
class TypeInline(admin.StackedInline):
    model = Type

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [RatingInline]

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Pricegroup)
admin.site.register(Type)
admin.site.register(Review)
admin.site.register(User)