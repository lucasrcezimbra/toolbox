from django.db.models import Count
from django.shortcuts import render
from taggit.models import Tag

from toolbox.core.models import List, Tool


def index(request):
    number_of_lists = List.objects.count()
    number_of_tools = Tool.objects.count()
    number_of_tags = Tag.objects.count()
    last_updated_lists = List.objects.order_by("-updated_at")[:10]
    random_tools = Tool.objects.all().order_by("?")[:5]
    tools = Tool.objects.all()[:20]
    return render(
        request,
        "index.html",
        {
            "number_of_lists": number_of_lists,
            "number_of_tags": number_of_tags,
            "number_of_tools": number_of_tools,
            "last_updated_lists": last_updated_lists,
            "random_tools": random_tools,
            "tools": tools,
        },
    )


def lists(request):
    lists = List.objects.annotate(number_of_tools=Count("tools")).all()
    return render(request, "lists.html", {"lists": lists})


def list_detail(request, slug):
    list = List.objects.get(slug=slug)
    tools = list.tools.all()
    return render(request, "list.html", {"list": list, "tools": tools})


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


def tag_detail(request, slug):
    tag = Tag.objects.get(slug=slug)
    tools = Tool.objects.filter(tags__slug=slug)
    number_of_tools = tools.count()
    return render(
        request,
        "tag.html",
        {"tag": tag, "number_of_tools": number_of_tools, "tools": tools[:100]},
    )


def tool_detail(request, slug):
    tool = Tool.objects.get(slug=slug)
    lists = tool.lists.all()
    related_tools = []
    for list in lists:
        related_tools.extend(list.tools.exclude(id=tool.id))
    return render(
        request,
        "tool.html",
        {"lists": lists, "related_tools": related_tools, "tool": tool},
    )
