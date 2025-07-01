from modeltranslation.translator import register, TranslationOptions
from .models import Regions, Hotel


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'tag', 'address')

@register(Regions)
class RegionsTranslationOptions(TranslationOptions):
    fields = ('name',)