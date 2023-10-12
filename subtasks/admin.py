from django.contrib import admin
from .models import SubTask


@admin.register(SubTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "team",
        "task",
    )

    search_fields = (
        "team",
        "task",
    )
