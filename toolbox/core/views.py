from django.db.models import Count
from django.shortcuts import render
from taggit.models import Tag

from toolbox.core.models import Tool


def index(request):
    number_of_tools = Tool.objects.count()
    number_of_tags = Tag.objects.count()
    tools = Tool.objects.order_by("-created_at")[:20]
    return render(
        request,
        "index.html",
        {
            "number_of_tags": number_of_tags,
            "number_of_tools": number_of_tools,
            "tools": tools,
        },
    )


def tags(request):
    tags = Tag.objects.annotate(number_of_tools=Count("tool")).order_by(
        "-number_of_tools"
    )
    return render(
        request,
        "tags.html",
        {
            "tags": tags,
        },
    )


def tag(request, slug):
    tags = Tag.objects.annotate(number_of_tools=Count("tool")).order_by(
        "-number_of_tools"
    )
    return render(
        request,
        "tags.html",
        {
            "tags": tags,
        },
    )
