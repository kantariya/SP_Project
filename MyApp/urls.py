from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('add-game/', views.add_game, name='add_game'),
    path('category/<str:category>/', views.category_games, name='category_games'),
]