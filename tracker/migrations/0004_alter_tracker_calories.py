# Generated by Django 4.2.5 on 2023-10-11 18:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0003_tracker_calories_alter_tracker_image_alt_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tracker",
            name="calories",
            field=models.FloatField(default="0"),
        ),
    ]
