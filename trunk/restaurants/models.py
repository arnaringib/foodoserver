from django.db import models

class User(models.Model):
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    apikey = models.CharField(max_length=40)
    
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
    
    def rating_range(self):
        return range(1,6)

    class Meta:
        ordering = ('name',)

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
    