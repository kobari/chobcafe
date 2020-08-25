from django.db import models
import jsonfield


class Places(models.Model):
    place_id = models.CharField(primary_key=True,
                                max_length=100)
    business_status = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    formatted_address = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=5,
                                 decimal_places=1)
    user_ratings_total = models.IntegerField()
    photos = jsonfield.JSONField(null=True)
    geometry = jsonfield.JSONField(null=True)
    types = jsonfield.JSONField(null=True)


class PlaceDetails(models.Model):
    place = models.ForeignKey(Places,
                              on_delete=models.CASCADE)
    url = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)
    photos = jsonfield.JSONField(null=True)
    reviews = jsonfield.JSONField(null=True)
    opening_hours = jsonfield.JSONField(null=True)
    address_components = jsonfield.JSONField(null=True)
