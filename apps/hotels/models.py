from django.contrib.auth import get_user_model
from django.db import models


Users = get_user_model()


class Regions(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20 , null=True, blank=True)
    phone_number_2 = models.CharField(max_length=20 , null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    image = models.ImageField()
    location_url = models.URLField(null=True, blank=True)
    tag = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
