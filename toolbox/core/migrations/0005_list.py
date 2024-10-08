# Generated by Django 5.1.1 on 2024-10-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_tool_added_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="List",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
    ]
