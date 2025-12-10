from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),  # keep real Django admin separate
    path('', include('animals.urls')),
]
