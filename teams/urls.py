from django.urls import path
from . import views

urlpatterns = [
    path("", views.Teams.as_view()),
]
