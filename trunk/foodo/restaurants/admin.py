from foodo.restaurants.models import Restaurant, Rating, Pricegroup, Type, Review, User, MenuItem, Order, OrderLine
from django.contrib import admin

class RatingInline(admin.StackedInline):
    model = Rating
    extra = 1
    
class TypeInline(admin.StackedInline):
    model = Type
    
class MenuInline(admin.TabularInline):
    model = MenuItem

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [RatingInline, MenuInline]
    list_display = ('__unicode__', 'qrcode')
    
#    list_display = ('name','rating_avg',)

class OrderLineInline(admin.TabularInline):
    model = OrderLine

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline,]

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Pricegroup)
admin.site.register(Type)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Order, OrderAdmin)