# Generated by Django 4.1.7 on 2023-03-21 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phoneNumber",
            field=models.BigIntegerField(max_length=16),
        ),
    ]
