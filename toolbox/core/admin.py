from django.contrib import admin

from toolbox.core.models import List, Tool


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tools",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "added_at", "url_github", "url_docs", "notes")
    ordering = ["-added_at"]
    search_fields = ("name",)
