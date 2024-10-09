from django.contrib import admin
from django.urls import path
from django_distill import distill_path

from toolbox.core.views import index, list_detail, lists, tags

urlpatterns = [
    path("admin/", admin.site.urls),
    distill_path("", index, name="index"),
    distill_path("lists/", lists, name="lists"),
    distill_path("lists/<str:slug>/", list_detail, name="list-detail"),
    distill_path("tags/", tags, name="tags"),
]
