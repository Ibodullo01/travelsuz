from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Hotel, Regions, HotelComment,HotelImage

admin.site.register(Hotel)
admin.site.register(Regions)
admin.site.register(HotelComment)
admin.site.register(HotelImage)
