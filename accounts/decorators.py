from django.http import HttpResponse
from django.shortcuts import redirect , render

from accounts.models import Employee

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request,*args,**kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None 
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('store')
            # HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request,*args,**kwargs):
        group = None 
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'customer':
            return redirect('store')
        if group == 'employee':
            return render(request,'accounts/authen.html')
        if group == 'admin':
            return view_func(request,*args,**kwargs)
        
    return wrapper_function
