# Generated by Django 3.2.8 on 2021-12-12 19:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lumisection_histos1D', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lumisectionhisto1d',
            name='data',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True), size=None),
        ),
    ]
