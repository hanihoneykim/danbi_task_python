from django.urls import path
from . import views

urlpatterns = [
    path("", views.Tasks.as_view()),
]
