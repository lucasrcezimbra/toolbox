from django.contrib import admin
from django.urls import path
from django_distill import distill_path

from toolbox.core.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    distill_path("", index, name="index"),
]
