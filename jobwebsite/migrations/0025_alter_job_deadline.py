# Generated by Django 5.1 on 2024-11-18 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0024_remove_jobskill_job_job_deadline_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="deadline",
            field=models.DateTimeField(),
        ),
    ]
