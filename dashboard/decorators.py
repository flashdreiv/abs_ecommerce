from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied

def admin_only(view_func):
    def wrapper_func(request, *args,**kwargs):
        group = None
        if request.user.is_superuser:
           return view_func(request, *args,**kwargs)
        else:
            return redirect('store')
    return wrapper_func
