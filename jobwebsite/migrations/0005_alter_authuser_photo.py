# Generated by Django 5.1 on 2024-10-04 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0004_remove_candidate_photo_authuser_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authuser",
            name="photo",
            field=models.ImageField(default="photo/default.png", upload_to="media/"),
        ),
    ]
