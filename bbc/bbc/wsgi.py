"""
WSGI config for bbc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/home/darkone0112/bolshoi-burglars-cinema')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbc.settings')

application = get_wsgi_application()
