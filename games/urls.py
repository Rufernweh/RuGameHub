from django.urls import path
from .views import *

app_name='games'
urlpatterns = [
    path('',index_view,name='index'),
    path('create-company/',create_company,name='create-company'),
    path('company-account/',company_account,name='company-account'),
    path('add-game-account/',add_game_account,name='add-game-account'),
    path('game-accounts/',game_accounts,name='game-accounts'),

    # path('',index_view,name='index'),
]
