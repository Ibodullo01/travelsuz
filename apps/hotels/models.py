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
    price = models.DecimalField(max_digits=10, decimal_places=2 )
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    location = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE , related_name='images')
    image = models.ImageField(upload_to='hotel_images')

    def __str__(self):
        return f"{self.hotel.title} - {self.image.name}"

class HotelComment(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.title_uz} - {self.text}"