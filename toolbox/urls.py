from django.contrib import admin
from django.urls import path
from django_distill import distill_path
from taggit.models import Tag

from toolbox.core.models import List, Tool
from toolbox.core.views import index, list_detail, lists, tag_detail, tags, tool_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    distill_path("", index, name="index"),
    distill_path("lists/", lists, name="lists"),
    distill_path(
        "lists/<str:slug>/",
        list_detail,
        name="list-detail",
        distill_func=lambda: (x.slug for x in List.objects.all()),
    ),
    distill_path("tags/", tags, name="tags"),
    distill_path(
        "tags/<str:slug>/",
        tag_detail,
        name="tag-detail",
        distill_func=lambda: (t.slug for t in Tag.objects.all()),
    ),
    distill_path(
        "tools/<str:slug>/",
        tool_detail,
        name="tool-detail",
        distill_func=lambda: (t.slug for t in Tool.objects.all()),
    ),
]
