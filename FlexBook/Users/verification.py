from functools import wraps
from django.shortcuts import redirect
from .models import Client


def user_valid(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.banned:
            return redirect('ban_page')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view


def user_is_buster(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_client = Client.objects.get(user=request.user)
            if user_client.client_info == user_client.BOOSTER:
                kwargs['booster'] = True
            elif user_client.client_info == user_client.CLIENT:
                kwargs['booster'] = False
        except TypeError:
            pass
        return view_func(request, *args, **kwargs)
    return _wrapped_view
