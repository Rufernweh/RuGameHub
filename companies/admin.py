from django.contrib import admin
from .models import Company


# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "code",'user')
    search_fields = ("name", "code",'user')


admin.site.register(Company,CompanyAdmin)