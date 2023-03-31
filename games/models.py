from django.db import models
from django.contrib.auth import get_user_model
from services.mixin import DateMixin,SlugMixin
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from services.choices import GAME_STATUS
from services.uploader import Uploader
from services.slugify import slugify
from services.generator import CodeGenerator
from companies.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

User=get_user_model()

class Category(DateMixin,SlugMixin,MPTTModel):
    name=models.CharField(max_length=40)
    icon=models.ImageField(upload_to=Uploader.upload_logo_game_category,blank=True,null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=('-created_at',)
        verbose_name='Game Category'
        verbose_name_plural='Game Categories'

    def save(self,*args,**kwargs):
        self.code=CodeGenerator.create_slug_shortcode(
            size=20,model_=Category
        )
        self.slug=slugify(self.name)

        return super().save(*args,**kwargs)


    

class GameAccount(DateMixin,SlugMixin):
    name=models.CharField(max_length=40)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    type=models.CharField(max_length=50,choices=GAME_STATUS,blank=True,null=True)
    description=RichTextField()
    price=models.PositiveIntegerField()
    mobile=PhoneNumberField(blank=True,null=True)
    is_active=models.BooleanField(default=True)

    

    def __str__(self):
        return self.name

    class Meta:
        ordering=('-created_at',)
        verbose_name='Game Account'
        verbose_name_plural='Game Accounts'

    


    def save(self,*args,**kwargs):
        self.code=CodeGenerator.create_slug_shortcode(
            size=20,model_=GameAccount
        )


        return super().save(*args,**kwargs)
    

class GameAccountGallery(DateMixin):
    game=models.ForeignKey(GameAccount,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=Uploader.upload_image_game)

    def __str__(self):
        return self.game.name

    class Meta:
        ordering=('-created_at',)
        verbose_name='Game Account Gallery'
        verbose_name_plural='Game Accounts Galleries'

  