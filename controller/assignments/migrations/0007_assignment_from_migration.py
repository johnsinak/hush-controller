# Generated by Django 5.0 on 2024-02-08 00:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("assignments", "0006_client_flagged"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="from_migration",
            field=models.BooleanField(default=False),
        ),
    ]