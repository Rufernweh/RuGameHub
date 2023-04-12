from django.db import models
from games.models import GameAccount
from services.mixin import DateMixin,SlugMixin
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.


class Basket(DateMixin):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    gameacc=models.OneToOneField(GameAccount,on_delete=models.CASCADE)


    class Meta:
        ordering=('-created_at',)
        verbose_name='Basket'

    def __str__(self):
        return f'{self.user.full_name} - {self.gameacc.name}'


