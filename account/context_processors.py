# context_processors.py

from django.conf import settings

def frontend_base_url(request):
    return {'FRONTEND_BASE_URL': settings.FRONTEND_BASE_URL}
