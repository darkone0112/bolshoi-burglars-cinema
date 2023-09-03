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

def play_movie(request, movie_title):
    try:
        movie_path = f"/path/to/{movie_title}.mp4"
        
        if not os.path.exists(movie_path):
            logger.error(f"Movie {movie_title} not found.")
            return HttpResponse('Movie not found', status=404)

        file_size = os.path.getsize(movie_path)
        start_range = 0
        end_range = file_size - 1

        if 'HTTP_RANGE' in request.META:
            http_range = request.META['HTTP_RANGE']
            start_range, end_range = [int(x) for x in http_range.replace('bytes=', '').split('-')]
            end_range = min(end_range, file_size - 1)
            response = StreamingHttpResponse(open(movie_path, 'rb'), status=206, content_type='video/mp4')
            response['Content-Length'] = end_range - start_range + 1
            response['Content-Range'] = f'bytes {start_range}-{end_range}/{file_size}'
        else:
            response = FileResponse(open(movie_path, 'rb'), content_type='video/mp4')
            response['Content-Length'] = file_size

        response['Accept-Ranges'] = 'bytes'
        logger.info(f"Streaming initiated for {movie_title}")

        return response

    except FileNotFoundError:
        logger.error(f"File {movie_path} not found.")
        return HttpResponse('File not found', status=404)

    except PermissionError:
        logger.error(f"Permission denied for {movie_path}.")
        return HttpResponse('Permission denied', status=403)

    except Exception as e:
        logger.error(f"An error occurred while streaming the movie: {str(e)}")
        return HttpResponse('Internal Server Error', status=500)