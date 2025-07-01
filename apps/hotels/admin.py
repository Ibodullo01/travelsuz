from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Hotel, Regions

admin.site.register(Hotel)
admin.site.register(Regions)
