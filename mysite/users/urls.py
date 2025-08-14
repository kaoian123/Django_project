from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("profile/public", views.profiles_public, name="profile_public"),
    path("profile/<slug:slug>", views.profile, name="profile"),
    path(
        "profile/<slug:slug>/export/pdf",
        views.profile_export_pdf,
        name="profile_export_pdf",
    ),
    path("api/", include("users.api.urls")),
]
