# Generated by Django 5.1 on 2024-10-04 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobwebsite", "0006_alter_authuser_photo_alter_candidate_resume_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authuser",
            name="photo",
            field=models.ImageField(default="photo/default.png", upload_to="photo/"),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="resume",
            field=models.FileField(default="resume/resume.pdf", upload_to="resume/"),
        ),
        migrations.AlterField(
            model_name="company",
            name="logo",
            field=models.ImageField(default="logo/logo.png", upload_to="logo/"),
        ),
    ]
