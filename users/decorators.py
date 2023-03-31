from django.shortcuts import redirect
from companies.models import Company



def not_authorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def not_created_company(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated and Company.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect("games:create-company")
    return wrapper_func
