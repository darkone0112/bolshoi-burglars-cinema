from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_movies, name='list_movies'),
    path('play_movie/<str:movie_title>/', views.play_movie, name='play_movie'),
]