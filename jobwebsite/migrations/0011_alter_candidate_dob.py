# Generated by Django 5.1 on 2024-10-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0010_rename_end_date_candidateeducation_end_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="dob",
            field=models.DateField(),
        ),
    ]
