from django.urls import path
from . import views

urlpatterns = [
    path("", views.MyTasks.as_view()),
]
