from django.db import models
from ckeditor.fields import RichTextField
from services.mixin import DateMixin,SlugMixin

# Create your models here.


class Contact(DateMixin):
    name=models.CharField(max_length=30,blank=True,null=True)
    email=models.EmailField(blank=True,null=True)
    message=RichTextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=('-created_at',)
        verbose_name='Contact'
        verbose_name_plural='Contacts'

