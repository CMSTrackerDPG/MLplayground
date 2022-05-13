# Generated by Django 4.0.3 on 2022-03-24 14:28

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("data_taking_objects", "0001_initial"),
        ("histogram_file_manager", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RunHistogram",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=220)),
                ("primary_dataset", models.CharField(max_length=220)),
                ("path", models.CharField(max_length=220)),
                ("entries", models.BigIntegerField(null=True)),
                ("mean", models.FloatField(null=True)),
                ("rms", models.FloatField(null=True)),
                ("skewness", models.FloatField(null=True)),
                ("kurtosis", models.FloatField(null=True)),
                (
                    "run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data_taking_objects.run",
                    ),
                ),
                (
                    "source_data_file",
                    models.ForeignKey(
                        blank=True,
                        help_text="Source data file that the specific Histogram was read from, if any",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="histogram_file_manager.histogramdatafile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LumisectionHistogram2D",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=220)),
                ("entries", models.IntegerField(blank=True, null=True)),
                (
                    "data",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(), blank=True, size=None
                    ),
                ),
                ("x_min", models.FloatField(blank=True, null=True)),
                ("x_max", models.FloatField(blank=True, null=True)),
                ("x_bin", models.IntegerField(blank=True, null=True)),
                ("y_max", models.FloatField(blank=True, null=True)),
                ("y_min", models.FloatField(blank=True, null=True)),
                ("y_bin", models.IntegerField(blank=True, null=True)),
                (
                    "lumisection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data_taking_objects.lumisection",
                    ),
                ),
                (
                    "source_data_file",
                    models.ForeignKey(
                        blank=True,
                        help_text="Source data file that the specific Histogram was read from, if any",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="histogram_file_manager.histogramdatafile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LumisectionHistogram1D",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=220)),
                ("entries", models.IntegerField(blank=True, null=True)),
                (
                    "data",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(), blank=True, size=None
                    ),
                ),
                ("x_min", models.FloatField(blank=True, null=True)),
                ("x_max", models.FloatField(blank=True, null=True)),
                ("x_bin", models.IntegerField(blank=True, null=True)),
                (
                    "lumisection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data_taking_objects.lumisection",
                    ),
                ),
                (
                    "source_data_file",
                    models.ForeignKey(
                        blank=True,
                        help_text="Source data file that the specific Histogram was read from, if any",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="histogram_file_manager.histogramdatafile",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="runhistogram",
            constraint=models.UniqueConstraint(
                fields=("run", "primary_dataset", "title"),
                name="unique run/dataset/histogram combination",
            ),
        ),
        migrations.AddConstraint(
            model_name="lumisectionhistogram2d",
            constraint=models.UniqueConstraint(
                fields=("lumisection", "title"),
                name="unique run / ls / 2d histogram combination",
            ),
        ),
        migrations.AddConstraint(
            model_name="lumisectionhistogram1d",
            constraint=models.UniqueConstraint(
                fields=("lumisection", "title"),
                name="unique run / ls / 1d histogram combination",
            ),
        ),
    ]
