from modeltranslation.translator import register, TranslationOptions
from .models import Travel


@register(Travel)
class TravelTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')

