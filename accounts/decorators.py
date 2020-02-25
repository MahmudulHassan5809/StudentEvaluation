from django.shortcuts import redirect
from django.contrib import messages


def active_user_required():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_profile.active:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, ('Please Login Or May Be Your Account Is Not Active'))
                return redirect('accounts:login')
        return wrap
    return decorator