from django.urls import path
from . import views

urlpatterns = [
    path("", views.SubTasks.as_view()),
    path("<int:pk>", views.SubTaskDetail.as_view()),
]
