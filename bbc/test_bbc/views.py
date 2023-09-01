from django.shortcuts import render
from django.http import FileResponse, HttpResponse
import json
import mimetypes
import os
def stream_video(request):
    return render(request, 'stream_video.html')

def list_movies(request):
    os.getcwd()
    with open('../../json/movies.json', 'r') as f:
        movies = json.load(f)
    return render(request, 'index.html', {'movies': movies})

def play_movie(request, movie_title):
    # Assuming you have a JSON file that maps movie titles to file paths
    with open('../../json/movies.json', 'r') as f:
        movies = json.load(f)

    # Find the correct movie path
    movie_path = None
    for movie in movies:
        if movie['title'] == movie_title:
            movie_path = movie['file_path']
            break

    # If movie was not found, return a 404 response
    if movie_path is None:
        return HttpResponse('Movie not found', status=404)

    # Return a FileResponse to stream the movie file
    return FileResponse(open(movie_path, 'rb'))