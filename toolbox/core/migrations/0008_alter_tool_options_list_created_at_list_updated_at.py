# Generated by Django 5.1.1 on 2024-10-11 20:54

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_tool_url_github"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tool",
            options={"ordering": ["-added_at"]},
        ),
        migrations.AddField(
            model_name="list",
            name="created_at",
            field=models.DateField(
                auto_now_add=True,
                default=datetime.datetime(
                    2024, 10, 11, 20, 54, 47, 732941, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="list",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
    ]