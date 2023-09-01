from django.shortcuts import render
import json
import mimetypes

def stream_video(request):
    return render(request, 'stream_video.html')

def list_movies(request):
    with open('test_bbc/json/movies.json', 'r') as f:
        movies = json.load(f)
    return render(request, 'index.html', {'movies': movies})

def play_movie(request, movie_title):
    with open('test_bbc/json/movies.json', 'r') as f:
        movies = json.load(f)
    movie_to_play = next((movie for movie in movies if movie['title'] == movie_title), None)
    if movie_to_play:
        file_path = movie_to_play['file_path']
        mime_type, encoding = mimetypes.guess_type(file_path)
        return render(request, 'play_movie.html', {'file_path': file_path, 'mime_type': mime_type})
    else:
        return render(request, 'error.html', {'message': 'Movie not found'})