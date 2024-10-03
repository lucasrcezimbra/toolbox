from django.db import models
from taggit.managers import TaggableManager


class Tool(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url_github = models.URLField()
    name = models.CharField(max_length=254)
    notes = models.TextField(blank=True)

    tags = TaggableManager()
