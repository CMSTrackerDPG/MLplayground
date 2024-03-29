# Generated by Django 4.1.1 on 2022-10-03 14:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("histograms", "0007_alter_lumisectionhistogram1d_lumisection_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lumisectionhistogram1d",
            options={"verbose_name_plural": "Lumisection Histograms 1D"},
        ),
        migrations.AlterModelOptions(
            name="lumisectionhistogram2d",
            options={"verbose_name_plural": "Lumisection Histograms 2D"},
        ),
        migrations.AlterField(
            model_name="lumisectionhistogram2d",
            name="data",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.FloatField(), blank=True, size=None
                ),
                blank=True,
                size=None,
            ),
        ),
    ]
