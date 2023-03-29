from django.db import models
from services.mixin import DateMixin,SlugMixin
from services.uploader import Uploader
from services.choices import PREMIUM_ACCOUNT
from services.generator import CodeGenerator
from services.slugify import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

User=get_user_model()
class Company(DateMixin,SlugMixin):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=True,null=True)
    icon=models.ImageField(upload_to=Uploader.upload_logo_game_company,blank=True,null=True)
    bio=RichTextField(blank=True,null=True)
    mobile=PhoneNumberField()
    VIP_status=models.CharField(max_length=40,choices=PREMIUM_ACCOUNT,blank=True,null=True)
    max_account_count=10


    def __str__(self):
        return self.name
    
    class Meta:
        ordering=('-created_at',)
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def save(self,*args,**kwargs):
        self.code=CodeGenerator.create_slug_shortcode(
            size=20,model_=Company
        )

        return super().save(*args,**kwargs)