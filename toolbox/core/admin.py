from django.contrib import admin

from toolbox.core.models import List, Tool


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tools",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ["-added_at"]
