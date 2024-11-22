# Generated by Django 5.1 on 2024-09-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="authuser",
            name="gender",
            field=models.CharField(
                choices=[("male", "male"), ("female", "female"), ("other", "other")],
                default="male",
                max_length=10,
            ),
        ),
    ]