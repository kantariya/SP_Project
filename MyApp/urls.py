from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
]