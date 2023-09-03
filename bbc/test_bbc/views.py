from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from wsgiref.util import FileWrapper
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

def play_movie(request, movie_title):
    logger.info(f"Received request to play movie: {movie_title}")

    # Assuming you have a JSON file that maps movie titles to file paths
    with open('/home/darkone0112/bolshoi-burglars-cinema/bbc/test_bbc/json/movies.json', 'r') as f:
        movies = json.load(f)

    # Find the correct movie path
    movie_path = None
    for movie in movies:
        if movie['title'] == movie_title:
            movie_path = movie['file_path']
            break

    # If movie was not found, return a 404 response
    if movie_path is None:
        logger.error(f"Movie {movie_title} not found.")
        return HttpResponse('Movie not found', status=404)

    # Get file size
    file_size = os.path.getsize(movie_path)
    logger.info(f"File size: {file_size}")

    # Handle ranges
    start_range = 0
    end_range = file_size - 1
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)

    if range_match:
        start_group, end_group = range_match.groups()
        if start_group is not None:
            start_range = int(start_group)
        if end_group is not None:
            end_range = int(end_group)

    logger.info(f"Start range: {start_range}, End range: {end_range}")

    # Set headers and stream the file
    response = StreamingHttpResponse(
        FileWrapper(open(movie_path, 'rb'), blksize=65536),  # Updated block size to 64KB
        status=206 if range_header else 200,
        content_type='video/mp4'
    )
    response['Content-Length'] = str(end_range - start_range + 1)
    response['Content-Range'] = f"bytes {start_range}-{end_range}/{file_size}"

    logger.info(f"Streaming initiated for {movie_title}")

    return response
