# Generated by Django 5.0.6 on 2024-10-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_tool_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tool",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]