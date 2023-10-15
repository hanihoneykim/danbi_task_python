from django.contrib import admin
from .models import SubTask


@admin.register(SubTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task",)

    search_fields = (
        "task",
        "team",
    )
