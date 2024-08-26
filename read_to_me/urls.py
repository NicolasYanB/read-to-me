from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('front.urls')),
    path('api/', include('core.urls'))
]
