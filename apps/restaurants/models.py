import datetime

from django.db import models
from apps.hotels.models import Regions
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE , null=True, blank=True)
    category = models.CharField(max_length=500)
    price_range = models.CharField(
        max_length=50,
        help_text="Arzon, O'rta, Qimmat"
    )
    opening_time = models.TimeField(default=datetime.time(9, 0), null=True, blank=True)
    closing_time = models.TimeField(default=datetime.time(21, 0), null=True, blank=True)
    location = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='restaurant_images')

    def __str__(self):
        return f"{self.restaurant.name} - {self.image.name}"


class RestaurantComments(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.restaurant.name)} - {self.comment} '