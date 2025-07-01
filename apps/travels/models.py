from django.db import models
from apps.hotels.models import Regions

# Create your

class Travel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='travel_images', null=True, blank=True)
    location_url = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=100)
    place_type = models.CharField(max_length=20)
    region = models.ForeignKey(Regions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)




