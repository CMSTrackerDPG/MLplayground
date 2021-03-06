# Generated by Django 4.0.3 on 2022-03-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HistogramDataFile",
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
                (
                    "filepath",
                    models.FilePathField(
                        help_text="Path where the file is stored",
                        match=".*\\.csv",
                        max_length=255,
                        path="/home/mpliax/Desktop/tmp",
                        recursive=True,
                    ),
                ),
                (
                    "filesize",
                    models.FloatField(
                        default=0, help_text="The data file's size (Mbytes)"
                    ),
                ),
                (
                    "data_dimensionality",
                    models.PositiveIntegerField(
                        blank=True, choices=[(1, "1D"), (2, "2D")], default=1
                    ),
                ),
                (
                    "data_era",
                    models.CharField(
                        blank=True,
                        help_text="The era that the data refers to (e.g. 2018A)",
                        max_length=5,
                    ),
                ),
                (
                    "entries_total",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Total number of entries contained in this histogram file",
                    ),
                ),
                (
                    "entries_processed",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Number of histogram entries that have been extracted from the file",
                    ),
                ),
                (
                    "granularity",
                    models.CharField(
                        choices=[("run", "Run"), ("lum", "Lumisection")],
                        default="run",
                        help_text="The granularity of the data contained in the data file (either whole run or lumisections)",
                        max_length=3,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name="histogramdatafile",
            constraint=models.UniqueConstraint(
                fields=("filepath",), name="unique_filepath"
            ),
        ),
    ]
