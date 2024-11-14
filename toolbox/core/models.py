from django.db import models
from taggit.managers import TaggableManager


class ToolManager(models.Manager):
    def get_by_natural_key(self, url_github):
        return self.get(url_github=url_github)


class Tool(models.Model):
    added_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    notes = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    url_docs = models.URLField(blank=True)
    url_github = models.URLField(unique=True)

    objects = ToolManager()
    tags = TaggableManager()

    class Meta:
        ordering = ["-added_at"]

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.url_github,)


class ListManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class List(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    tools = models.ManyToManyField(Tool, related_name="lists")

    objects = ListManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)
