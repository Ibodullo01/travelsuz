from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)

