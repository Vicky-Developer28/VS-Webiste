def google_analytics(request):
    from django.conf import settings
    return {'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID}
