from django.db import models
from django.db.models import Avg
import math

class User(models.Model):
    firstName = models.CharField(max_length=40, blank=True)
    lastName = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    apikey = models.CharField(max_length=40, blank=True, unique=True)
    
    def __unicode__(self):
        return "%s %s (%s)" % (self.firstName, self.lastName, self.email)

class Pricegroup(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        
class Type(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)

class Restaurant(models.Model):
    """docstring for Restaurant"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=32)
    address = models.CharField(max_length=40)
    zip = models.IntegerField()
    city = models.CharField(max_length=30)
    website = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    lat = models.IntegerField()
    lng = models.IntegerField()
    created = models.DateTimeField('date created')
    
    pricegroup = models.ForeignKey(Pricegroup)
    types = models.ManyToManyField(Type, blank=True)
    
    def __unicode__(self):
        return self.name
        
    def is_rating_valid(self,rating):
        return (rating in range(1,6))
        
    def qrcode(self):
        return "<a href='http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=http://foodo.morpho.nord.is/m/restaurants/%d/' target='_blank'>QR Code</a>" % self.id
    qrcode.allow_tags = True
    
    def distanceFrom(self, lat, lng):
        lat1 = float(self.lat)/1000000.0
        lon1 = float(self.lng)/1000000.0
        lat2 = float(lat)
        lon2 = float(lng)
        
        x = (math.sin(lat1/57.2958) * math.sin(lat2/57.2958)) + (math.cos(lat1/57.2958) * math.cos(lat2/57.2958) * math.cos(lon2/57.2958 - lon1/57.2958))
        d = 6378.8 * math.atan(math.sqrt(1-x**2)/x)
        return d

    class Meta:
        ordering = ('name',)
        
def get_restaurantlogo_name(instance, filename):
    return 'logo/%i.jpg' % instance.restaurant.id

class RestaurantLogo(models.Model):
    logo = models.FileField(upload_to=get_restaurantlogo_name)
    restaurant = models.OneToOneField(Restaurant)

class Review(models.Model):
    description = models.TextField(blank=True)
    created = models.DateTimeField('date created')
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User)
        
    def __unicode__(self):
        return "Review for %s" % self.restaurant.name
        
class Rating(models.Model):
    rating = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)

class MenuItem(models.Model):    
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant)
    
    def __unicode__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    created = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField()
    notified = models.BooleanField()

    def __unicode__(self):
        return "#%d - Order for %s" % (self.pk, self.restaurant.name)
    
class OrderLine(models.Model):
    item = models.ForeignKey(MenuItem)
    order = models.ForeignKey(Order)
    count = models.IntegerField()
    price = models.IntegerField()

class Notification(models.Model):
    order = models.ForeignKey(Order)
    message = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now=True)
