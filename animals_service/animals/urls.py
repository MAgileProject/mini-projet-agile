from django.urls import path
from . import views

urlpatterns = [
    # Client
    path("", views.catalog_view, name="catalog"),
    path("animals/<int:pk>/", views.animal_detail, name="animal_detail"),
    path("animals/propose/", views.client_propose_animal, name="client_propose_animal"),

    # Admin
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/manage/", views.admin_manage_animals, name="admin_manage_animals"),
    path("admin/pending/", views.admin_pending, name="admin_pending"),

    # API
    path("api/animals/", views.AnimalListCreateAPI.as_view(), name="api_animals"),
    path("api/animals/<int:pk>/", views.AnimalRetrieveUpdateDestroyAPI.as_view()),
path(
    "api/animals/<int:pk>/adopt/",
    views.request_adoption_api,
    name="api_animal_adopt"
),
    # Admin actions
    path("api/admin/animals/<int:pk>/approve/", views.approve_animal_api),
    path("api/admin/animals/<int:pk>/reject/", views.reject_animal_api),
]
