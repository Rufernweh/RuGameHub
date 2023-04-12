from django.contrib import admin
from .models import Basket


# Register your models here.

class BasketAdmin(admin.ModelAdmin):
    list_display=['user','gameacc']

admin.site.register(Basket,BasketAdmin)