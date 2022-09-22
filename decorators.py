from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect

from accounts.models import MyUser


def is_admin():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if not user.is_blocked:
                    if user.is_admin:
                        return view_function(request, *args, **kwargs)
                    else:
                        raise PermissionDenied
                else:
                    auth.logout(request)
                    return HttpResponse('Your account is blocked. Please contact admin')
            else:
                return redirect('accounts:login')

        return wrap

    return decorator


def is_login():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if not user.is_blocked:
                    return view_function(request, *args, **kwargs)
                else:
                    auth.logout(request)
                    return HttpResponse('Your account is blocked. Please contact admin')
            else:
                return redirect('accounts:login')

        return wrap

    return decorator
