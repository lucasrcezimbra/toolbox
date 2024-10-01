from django.shortcuts import render

from toolbox.core.models import Tool


def index(request):
    tools = Tool.objects.order_by("-created_at")[:20]
    total = Tool.objects.count()
    return render(request, "index.html", {"tools": tools, "total": total})
