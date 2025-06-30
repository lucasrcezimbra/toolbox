from django.core.serializers import deserialize


def run():
    with open("data/partial_tools_notes.json", "r") as f:
        for deserialized in deserialize("json", f):
            try:
                deserialized.object.save(update_fields=["notes"])
            except Exception as e:
                print("Failed to import:", deserialized.object.url_github)
                raise e

