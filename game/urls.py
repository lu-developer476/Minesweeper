from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/new", views.api_new_game, name="api_new_game"),
    path("api/reveal", views.api_reveal, name="api_reveal"),
    path("api/toggle-flag", views.api_toggle_flag, name="api_toggle_flag"),
]
