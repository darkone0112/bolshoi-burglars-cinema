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

from django.http import FileResponse, HttpResponse, StreamingHttpResponse
import os
import json
import logging

# Initialize logging
logger = logging.getLogger(__name__)

from django.http import FileResponse, HttpResponse, StreamingHttpResponse
import os
import json
import logging

# Initialize logging
logger = logging.getLogger(__name__)

def file_iterator(file_path, start_byte, end_byte, chunk_size=8192):
    with open(file_path, 'rb') as f:
        f.seek(start_byte)
        while start_byte <= end_byte:
            data = f.read(min(chunk_size, end_byte - start_byte + 1))
            if not data:
                break
            start_byte += len(data)
            yield data

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

        start_byte = 0
        end_byte = file_size - 1

        if 'HTTP_RANGE' in request.META:
            range_header = request.META['HTTP_RANGE'].split("bytes=")[1]
            start_byte, end_byte_str = map(str, range_header.split("-"))
            start_byte = int(start_byte)
            end_byte = int(end_byte_str) if end_byte_str else file_size - 1
            end_byte = min(end_byte, file_size - 1)

            response = StreamingHttpResponse(
                file_iterator(movie_path, start_byte, end_byte),
                status=206,
                content_type='video/mp4'
            )
            response['Content-Range'] = f"bytes {start_byte}-{end_byte}/{file_size}"
        else:
            response = StreamingHttpResponse(
                file_iterator(movie_path, start_byte, end_byte),
                content_type='video/mp4'
            )

        response['Content-Length'] = end_byte - start_byte + 1
        response['Accept-Ranges'] = 'bytes'

        logger.info(f"Streaming initiated for {movie_title}")

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)
        if range_match:
            start, end = range_match.groups()
            logger.info(f"Range request: start={start}, end={end}")
        else:
            logger.info(f"No valid range request found: {range_header}")

        return response

    except Exception as e:
        logger.error(f"An error occurred while streaming the movie: {str(e)}")
        return HttpResponse('Internal Server Error', status=500)

