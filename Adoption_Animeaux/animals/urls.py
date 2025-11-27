from django.urls import path
from . import views

app_name = "animals"

urlpatterns = [
    path('', views.AnimalListView.as_view(), name='list'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='detail'),

    # CRUD admin
    path('add/', views.AnimalCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', views.AnimalUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.AnimalDeleteView.as_view(), name='delete'),
]
