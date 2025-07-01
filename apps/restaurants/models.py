import datetime

from django.db import models
from apps.hotels.models import Regions
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    price_range = models.CharField(
        max_length=50,
        help_text="Arzon, O'rta, Qimmat"
    )
    opening_time = models.TimeField(default=datetime.time(9, 0), null=True, blank=True)
    closing_time = models.TimeField(default=datetime.time(21, 0), null=True, blank=True)
    image = models.ImageField(upload_to='restaurants/')
    location_url = models.URLField(null=True, blank=True)
    tag = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

