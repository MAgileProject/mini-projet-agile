from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    index,
    register,
    login_view, logout_view,
    home, profile, delete_account,
    admin_dashboard, admin_edit_user, toggle_user_status, admin_delete_user
)

urlpatterns = [
    # Default → go to login page
    path("", login_view, name="login_default"),

    # Auth
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),

    # User pages
    path("home/", home, name="home"),
    path("profile/", profile, name="profile"),
    path("delete-account/", delete_account, name="delete_account"),

    # Admin pages
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path("admin-panel/users/<int:user_id>/edit/", admin_edit_user, name="admin_edit_user"),
    path("admin-panel/users/<int:user_id>/toggle-active/", toggle_user_status, name="toggle_user_status"),
    path("admin-panel/users/<int:user_id>/delete/", admin_delete_user, name="admin_delete_user"),

    # Django admin
    path("admin/", admin.site.urls),

    # REST API
    path("api/accounts/", include("accounts.urls")),
]
