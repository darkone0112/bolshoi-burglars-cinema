from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from wsgiref.util import FileWrapper
from django.http import FileResponse
import re
import os
import json
import logging

def stream_video(request):
    return render(request, 'stream_video.html')

def list_movies(request):
    os.getcwd()
    with open('/home/darkone0112/bolshoi-burglars-cinema/bbc/test_bbc/json/movies.json', 'r') as f:
        movies = json.load(f)
    return render(request, 'index.html', {'movies': movies})

# Initialize logging
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

from django.http import FileResponse, HttpResponse
import os
import json
import logging

# Initialize logging
logger = logging.getLogger(__name__)

def play_movie(request, movie_title):
    try:
        logger.info(f"Received request to play movie: {movie_title}")

        with open('/home/darkone0112/bolshoi-burglars-cinema/bbc/test_bbc/json/movies.json', 'r') as f:
            movies = json.load(f)

        movie_path = next((movie['file_path'] for movie in movies if movie['title'] == movie_title), None)

        if movie_path is None:
            logger.error(f"Movie {movie_title} not found.")
            return HttpResponse('Movie not found', status=404)

        file_size = os.path.getsize(movie_path)
        logger.info(f"File size: {file_size}")

        response = FileResponse(open(movie_path, 'rb'), content_type='video/mp4')

        logger.info(f"Streaming initiated for {movie_title}")
        return response

    except Exception as e:
        logger.error(f"An error occurred while streaming the movie: {str(e)}")
        return HttpResponse('Internal Server Error', status=500)
