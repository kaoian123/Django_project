from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("profile/<slug:slug>", views.profile, name="profile"),
]
