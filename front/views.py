import os

from django.shortcuts import render

def index(request):
  host = os.environ.get('HOST_URL')
  if host is None:
    host = 'http://localhost:8000'
  return render(request, 'index.html', {'host_url': host})