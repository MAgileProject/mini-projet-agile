from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("animals/", views.go_animals),
]
