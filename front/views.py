import os

from django.shortcuts import render

def index(request):
  host = request.META['HTTP_HOST']
  return render(request, 'index.html', {'host_url': host})