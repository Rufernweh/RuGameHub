from django.urls import path
from .views import *

app_name='games'
urlpatterns = [
    path('',index_view,name='index'),
    path('create-company/',create_company,name='create-company'),
    path('company-account/',company_account,name='company-account'),
    path('add-game-account/',add_game_account,name='add-game-account'),
    path('your-game-accounts/',user_game_accounts,name='user-game-accounts'),
    path('game-accounts-list/',list_view,name='game-accounts-list'),
    path('game-account-detail/<code>',detail_view,name='game-account-detail'),
    path('game-account-review/',add_comment,name='game-account-review'),
    path('check_login_status/',check_login_status,name='check-login-status'),

    # path('',index_view,name='index'),
]
