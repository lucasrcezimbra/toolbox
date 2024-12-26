import jsonstar as json

from toolbox.core.models import Tool


def run():
    tools = (
        Tool.objects.annotate(tags="tags")
        .values("url_github", "notes", "tags__slug")
        .all()
    )

    with open("data/partial_tools.json", "w") as f:
        f.writelines(json.dumps([t for t in tools], indent=4))
