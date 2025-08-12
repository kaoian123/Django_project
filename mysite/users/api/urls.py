from django.urls import path
from users.api import views

urlpatterns = [
    path("public-profiles/", views.public_profile_list, name="public-profile-list"),
]
