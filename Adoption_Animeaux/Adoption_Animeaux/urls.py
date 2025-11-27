from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),      # créer plus tard
    path('animals/', include('animals.urls')),
    path('adoptions/', include('adoptions.urls')),
    path('appointments/', include('appointments.urls')),
    path('', include('animals.urls')),                # home -> animaux
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
