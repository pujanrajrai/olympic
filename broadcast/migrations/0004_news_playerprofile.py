# Generated by Django 4.1.1 on 2022-09-23 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("broadcast", "0003_broadcast_total_view"),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("picture", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.CreateModel(
            name="PlayerProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("profile", models.ImageField(upload_to="profile/")),
                ("desc", models.TextField()),
            ],
        ),
    ]
