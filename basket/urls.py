from django import urls
from django.urls import path
from .views import *

app_name='basket'


urlpatterns = [
    path('remove-gameacc/',remove_gameacc,name='remove-gameacc'),
    path('',basket_view,name='basket'),
]   
