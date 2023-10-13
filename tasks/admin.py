from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "create_user",
        "team",
    )

    search_fields = (
        "title",
        "=create_user__username",
    )
