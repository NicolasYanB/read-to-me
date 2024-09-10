import os

from django.shortcuts import render

def index(request):
  host = request.META['HTTP_HOST']
  if os.environ.get('SECURE') == '1':
    scheme = 'https'
  else:
    scheme = 'http'
  return render(request, 'index.html', {'host_url': f'{scheme}://{host}'})