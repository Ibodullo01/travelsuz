from modeltranslation.translator import register, TranslationOptions
from .models import Regions, Restaurant


@register(Restaurant)
class RestaurantTranslationOptions(TranslationOptions):
    fields = ('name', 'description','address', 'category' , 'price_range')
