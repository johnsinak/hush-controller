# Generated by Django 5.0 on 2024-02-08 00:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("assignments", "0007_assignment_from_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="proxy",
            name="deactivated_at",
            field=models.IntegerField(default=0),
        ),
    ]
