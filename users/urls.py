from django.urls import path
from . import views


app_name='users'

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.password_change_view, name="change-password"),
    path("reset/", views.reset_password_view, name="reset"),
    path("reset-complete/<slug>/", views.reset_password_complete_view, name="reset-complete"),
    path("activate/<slug>/", views.account_activate_view, name="activate"),
    path('profile/',views.edit_profile,name='profile'),
]