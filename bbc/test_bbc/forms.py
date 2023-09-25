# forms.py
from django import forms

class MovieUploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    image_url = forms.URLField(max_length=500)
    movie_file = forms.FileField()
