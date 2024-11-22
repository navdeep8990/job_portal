# Generated by Django 5.1 on 2024-10-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0003_candidate_photo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="candidate",
            name="photo",
        ),
        migrations.AddField(
            model_name="authuser",
            name="photo",
            field=models.ImageField(default="photo/default.png", upload_to="photo/"),
        ),
    ]