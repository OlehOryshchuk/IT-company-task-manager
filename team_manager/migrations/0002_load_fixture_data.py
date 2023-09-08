# Generated by Django 4.2.5 on 2023-09-08 15:10

from django.core.management import call_command
from django.db import migrations

from IT_company_task_manager.settings import TESTING


def load_data(apps, schema_editor):
    call_command("loaddata", "fixture_data.json")


def reverse_load_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("team_manager", "0001_initial"),
    ]
    if not TESTING:
        # do not load fixture if we are running test
        operations = [migrations.RunPython(load_data, reverse_load_data)]
