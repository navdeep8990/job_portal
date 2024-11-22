# Generated by Django 5.1 on 2024-10-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0005_alter_authuser_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authuser",
            name="photo",
            field=models.ImageField(
                default="photo/default.png", upload_to="media/images/"
            ),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="resume",
            field=models.FileField(
                default="resume/resume.pdf", upload_to="media/resume/"
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="logo",
            field=models.ImageField(default="logo/logo.png", upload_to="media/logo/"),
        ),
    ]
