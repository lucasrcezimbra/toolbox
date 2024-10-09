from django.contrib import admin

from toolbox.core.models import List, Tool


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tool)
