from django.core.exceptions import PermissionDenied
from .models import *

def user_is_ad_owner(function):
    def wrap(request, *args, **kwargs):
        ad = Ad.objects.get(pk=kwargs['ad_id'])
        if ad.owner == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap