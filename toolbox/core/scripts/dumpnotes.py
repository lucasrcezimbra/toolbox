from django.core.serializers import serialize

from toolbox.core.models import Tool


def run():
    tools = Tool.objects.exclude(notes="")

    with open("data/partial_tools_notes.json", "w") as f:
        serialize(
            "json",
            tools,
            fields=("url_github", "notes"),
            indent=4,
            stream=f,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
        )
