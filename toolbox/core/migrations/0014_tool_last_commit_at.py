# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_tool_forks_tool_stargazers"),
    ]

    operations = [
        migrations.AddField(
            model_name="tool",
            name="last_commit_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]