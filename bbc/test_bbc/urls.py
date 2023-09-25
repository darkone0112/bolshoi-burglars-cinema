from django.urls import path
from .views import list_movies, play_movie, upload_movie

urlpatterns = [
    path('', list_movies, name='list_movies'),
    path('play_movie/<str:movie_title>/', play_movie, name='play_movie'),
    path('upload/', upload_movie, name='upload_movie')
]