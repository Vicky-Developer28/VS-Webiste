# middleware.py
from django.utils.deprecation import MiddlewareMixin
from main.models import Visitor
from django.utils import timezone

class CaptureIPAddressMiddleware(MiddlewareMixin):
    def get_client_ip(self, request):
        """ Extract the client IP from request headers """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # First IP in list (client's IP)
        else:
            ip = request.META.get('REMOTE_ADDR')  # Direct IP
        return ip

    def process_request(self, request):
        """ Store the IP address in the Visitor model """
        ip_address = self.get_client_ip(request)

        # Check if visitor already exists
        visitor, created = Visitor.objects.get_or_create(ip_address=ip_address)
        visitor.last_seen = timezone.now()
        visitor.save()
