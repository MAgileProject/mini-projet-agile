from django.contrib import admin
from django.urls import path, include
from . import views   

urlpatterns = [
    path('admin/', admin.site.urls),

    # Page d’accueil
    path('', views.home, name='home'),

    # Exemple : urls des animaux
    path('animals/', include('animals.urls')),
    path('accounts/', include('accounts.urls')),
]
