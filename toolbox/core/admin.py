from django.contrib import admin
from django.contrib.admin.options import format_html

from toolbox.core.models import List, Tool


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tools",)
    list_display = ("name", "slug", "count_tools", "created_at", "updated_at")
    ordering = ["slug"]
    prepopulated_fields = {"slug": ("name",)}

    def count_tools(self, obj):
        return obj.tools.count()

    count_tools.short_description = "Number of tools"


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "count_lists",
        "added_at",
        "url_github_html",
        "url_docs_html",
        "notes",
    )
    list_filter = (
        ("notes", admin.EmptyFieldListFilter),
        ("url_docs", admin.EmptyFieldListFilter),
    )
    ordering = ["-added_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def count_lists(self, obj):
        return obj.lists.count()

    count_lists.short_description = "Number of lists"

    def url_github_html(self, obj):
        return format_html(
            f"<a href='{obj.url_github}' target='_blank'>{obj.url_github.lstrip('https://github.com/')}</a>"
        )

    url_github_html.short_description = "URL GitHub"

    def url_docs_html(self, obj):
        return format_html(
            f"<a href='{obj.url_docs}' target='_blank'>{obj.url_docs}</a>"
        )

    url_github_html.short_description = "URL Docs"
