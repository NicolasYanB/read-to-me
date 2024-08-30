from django.urls import path

from . import views

urlpatterns = [
  path('extract', views.extract, name='extract'),
  path('generate', views.generate, name='generate')
]