from django.db import models
from taggit.managers import TaggableManager


class Tool(models.Model):
    added_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url_github = models.URLField()
    name = models.CharField(max_length=254)
    notes = models.TextField(blank=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class List(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    tools = models.ManyToManyField(Tool)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)
