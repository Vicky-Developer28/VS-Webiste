# utils.py
def get_client_ip(request):
    """Get the IP address of the visitor."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get the first IP in case of multiple
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
