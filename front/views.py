import os

from django.shortcuts import render

def index(request):
  host = request.META['HTTP_HOST']
  scheme = request.scheme
  return render(request, 'index.html', {'host_url': f'{scheme}://{host}'})