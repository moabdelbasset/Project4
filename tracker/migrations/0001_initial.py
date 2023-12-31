# Generated by Django 4.2.5 on 2023-10-03 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import djrichtextfield.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tracker",
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
                ("title", models.CharField(max_length=300)),
                (
                    "description",
                    djrichtextfield.models.RichTextField(blank=True, null=True),
                ),
                ("date", models.DateField()),
                ("calories", models.PositiveIntegerField()),
                (
                    "portion_size",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "meal_type",
                    models.CharField(
                        choices=[
                            ("Breakfast", "Breakfast"),
                            ("Lunch", "Lunch"),
                            ("Dinner", "Dinner"),
                            ("Snack", "Snack"),
                        ],
                        default="Snack",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        quality=75,
                        scale=None,
                        size=(400, None),
                        upload_to="tracker/",
                    ),
                ),
                ("image_alt", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracker_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
    ]
