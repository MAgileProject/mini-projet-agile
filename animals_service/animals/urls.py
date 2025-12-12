from django.urls import path
from . import views

urlpatterns = [
    # =====================
    # USER (client)
    # =====================
    path("", views.catalog_view, name="catalog"),
    path("animals/<int:pk>/", views.animal_detail, name="animal_detail"),
    path("animals/propose/", views.client_propose_animal, name="client_propose_animal"),

    # =====================
    # ADMIN (pages)
    # =====================
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/manage/", views.admin_manage_animals, name="admin_manage_animals"),
    path("admin/pending/", views.admin_pending, name="admin_pending"),
    path("admin/reserved/", views.admin_reserved_animals, name="admin_reserved_animals"),
    path("admin/adopted/", views.admin_adopted_animals, name="admin_adopted_animals"),
    path("admin/delete/<int:pk>/", views.admin_delete_animal, name="admin_delete_animal"),
    path("admin/edit/<int:pk>/", views.admin_edit_animal, name="admin_edit_animal"),

    # =====================
    # API (REST)
    # =====================
    path("api/animals/", views.AnimalListCreateAPI.as_view(), name="api_animals"),
    path("api/animals/<int:pk>/", views.AnimalRetrieveUpdateDestroyAPI.as_view()),
    path("api/animals/<int:pk>/adopt/", views.request_adoption_api, name="api_animal_adopt"),

    # Admin API
    path("api/admin/animals/<int:pk>/approve/", views.approve_animal_api),
    path("api/admin/animals/<int:pk>/reject/", views.reject_animal_api),
]
