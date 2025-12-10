from django.contrib import admin
from django.urls import path, include
from adoption.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('adoption/', include('adoption.urls')),
]
