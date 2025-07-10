from django.db import models
from apps.hotels.models import Regions

# Create your

class Travel(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    location = models.JSONField(null=True, blank=True)
    regions = models.ManyToManyField(Regions, related_name='travels')
    address = models.CharField(max_length=500)
    region = models.ForeignKey(Regions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} '


class TravelImage(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='travel_images/')

    def __str__(self):
        return f'{self.travel.title} - {self.image} '


class TravelComments(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.travel.title} - {self.comment} '