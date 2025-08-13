from django.urls import path
from users.api import views

urlpatterns = [
    path("public-profiles/", views.public_profile_list, name="public-profile-list"),
    path(
        "original-public-profiles/",
        views.original_public_profile_list,
        name="original-public-profile-list",
    ),
]
