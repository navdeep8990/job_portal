# Generated by Django 5.1 on 2024-10-15 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0008_remove_candidateeducation_percentage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidateeducation",
            name="end_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="candidateeducation",
            name="start_date",
            field=models.DateField(),
        ),
    ]
