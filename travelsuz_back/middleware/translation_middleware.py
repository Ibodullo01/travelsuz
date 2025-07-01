
from django.utils import translation

class TranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.headers.get('Accept-Language', 'uz').lower()
        if lang not in ['uz', 'ru', 'en']:
            lang = 'uz'


        with translation.override(lang):
            response = self.get_response(request)

        return response
