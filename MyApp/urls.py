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
    path('game/<int:game_id>/add_review/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('review/update/<int:review_id>/', views.update_review, name='update_review'),
    path('my-games/', views.my_games, name='my_games'),
    path('game/<int:pk>/update/', views.update_game, name='update_game'),
    path('game/<int:pk>/delete/', views.delete_game, name='delete_game'),
]