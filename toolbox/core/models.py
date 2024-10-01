from django.db import models


class Tool(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url_github = models.URLField()
    name = models.CharField(max_length=254)
    notes = models.TextField(null=True)
