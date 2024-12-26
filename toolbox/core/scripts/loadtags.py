from django.core.serializers import deserialize


def run():
    with open("data/partial_tools_notes.json", "r") as f:
        for deserialized in deserialize("json", f):
            print("[DEBUG]", deserialized.object.url_github)
            deserialized.object.save(update_fields=["notes"])
            deserialized.object.tags.add(deserialized.tags)
