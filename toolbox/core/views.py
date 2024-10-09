from django.db.models import Count
from django.shortcuts import render
from taggit.models import Tag

from toolbox.core.models import List, Tool


def index(request):
    number_of_tools = Tool.objects.count()
    number_of_tags = Tag.objects.count()
    tools = Tool.objects.order_by("-added_at")[:20]
    return render(
        request,
        "index.html",
        {
            "number_of_tags": number_of_tags,
            "number_of_tools": number_of_tools,
            "tools": tools,
        },
    )


def lists(request):
    lists = List.objects.all()
    return render(request, "lists.html", {"lists": lists})


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
