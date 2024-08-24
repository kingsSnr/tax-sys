# Generated by Django 4.2.13 on 2024-08-24 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taxes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="taxrecord",
            name="quarterly_payments",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="taxrecord",
            name="section_179_deduction",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
