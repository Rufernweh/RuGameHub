from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import (
    LoginForm, RegisterForm, ActivateForm, CustomPasswordChangeForm,
    ResetPasswordForm, ResetPasswordCompleteForm,UserProfileForm
)
from django.contrib.auth.decorators import login_required
from .decorators import not_authorized_user
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy

# Create your views here.

User = get_user_model()

def login_view(request):

    form_type = request.POST.get("form_type")
    login_form=LoginForm()
    next = request.GET.get("next", None)
    
    if form_type == "login":
        login_form = LoginForm(request.POST or None)

        if request.method == "POST" and login_form.is_valid():
            email = login_form.cleaned_data.get("email")
            password = login_form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            logout(request)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/')

    context = {
        "login_form":login_form,   
    }
    return render(request, "users/login.html", context)



def register(request):
    context={}
    register_form=RegisterForm()

    if  request.method == "POST":
        register_form = RegisterForm(request.POST or None)

        if  register_form.is_valid():
            user = register_form.save()

            return redirect("users:activate", slug=user.slug)
        
    context['form']=register_form
    return render(request,'users/register.html',context)


def logout_view(request):
    logout(request)
    return redirect('/')




 



def account_activate_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ActivateForm()
    error_message=''

    if request.method == "POST":
        form = ActivateForm(request.POST or None)

        if form.is_valid():
            if form.cleaned_data.get('activation_code') == user.activation_code:
                form.save(commit=False)
                user.is_active = True
                user.activation_code = None
                user.save()
                login(request, user)
                messages.success(request, 'Your account has been activated!')
                return redirect('/')
            else:
                error_message='This code is wrong'


    context = {
        "form": form,
        'error':error_message
    }
    return render(request, "users/activate.html", context)



@login_required(login_url='/users/login/')
def password_change_view(request):
    form = CustomPasswordChangeForm(user=request.user)

    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')

    context = {
        "form": form
        
    }
    return render(request, "users/password_change.html", context)



def reset_password_view(request):
    form = ResetPasswordForm()

    if request.method == "POST":
        form = ResetPasswordForm(request.POST or None)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            

            link = request.build_absolute_uri(reverse_lazy("users:reset-complete", kwargs={"slug": user.slug}))
            message = f"Please click the link below \n{link}"


            # send mail
            send_mail(
                'Reset password',  # subject
                message,  # message
                settings.EMAIL_HOST_USER,  # from email
                [email],  # to mail list
                fail_silently=False,
            )

            return redirect("/users/login/")

    context = {
        "form": form
    }
    return render(request, "users/reset.html", context)



def reset_password_complete_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ResetPasswordCompleteForm(instance=user)

    if request.method == "POST":

        form = ResetPasswordCompleteForm(instance=user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("/users/login/")

    context = {
        "form": form
    }
    return render(request, 'users/reset_complete.html', context)




@login_required(login_url='/users/login/')
def edit_profile(request):
    messages=''
    print(request.user)
    if request.user.is_anonymous:
        return redirect('users:login')
    else:
        form=UserProfileForm(instance=request.user,user=request.user)
        if request.method == 'POST':
            form=UserProfileForm(request.user,request.POST)
            if form.is_valid():
                messages='Successfull profile updated'
                form.save()
                return render(request, 'users/profile.html', {'form':form,'messages':messages})



    return render(request,'users/profile.html',{'form':form,'messages':messages})