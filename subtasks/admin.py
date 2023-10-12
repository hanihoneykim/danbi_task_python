from django.contrib import admin
from .models import SubTask


@admin.register(SubTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "task",
    )

    search_fields = (
        "task",
        "team",
    )
