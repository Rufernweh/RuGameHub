from django.contrib import admin
from .models import GameAccount,GameAccountGallery,Category,Review

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug", "code")
    search_fields = ("name", "code")


admin.site.register(Category,CategoryAdmin)

class ImageInline(admin.TabularInline):
    model = GameAccountGallery
    extra = 1

class GameAccountAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)
    list_display = ("name",  "slug", "code",'price')
    search_fields = ("name", "code",'price')

admin.site.register(GameAccount,GameAccountAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug", "code")
    search_fields = ("name", "code")

admin.site.register(GameAccountGallery,)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "message")


admin.site.register(Review,ReviewAdmin)
