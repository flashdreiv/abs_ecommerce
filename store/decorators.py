
from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied

def unverified_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.customer.verified:
            return view_func(request, *args,**kwargs)
        else:
            return redirect('sms-verification')
    return wrapper_func



