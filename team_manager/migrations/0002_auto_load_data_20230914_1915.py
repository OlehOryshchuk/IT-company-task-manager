from django.core.management import call_command
from django.db import migrations

from it_company_task_manager.settings import TESTING


def load_data(apps, schema_editor):
    call_command("loaddata", "project_data.json")


def reverse_load_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("team_manager", "0001_initial"),
    ]
    if not TESTING:
        # do not load fixture if we are running test
        operations = [migrations.RunPython(load_data, reverse_load_data)]
