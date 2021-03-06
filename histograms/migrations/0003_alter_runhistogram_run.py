# Generated by Django 3.2.8 on 2022-04-29 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("data_taking_objects", "0002_auto_20220429_0713"),
        ("histograms", "0002_alter_runhistogram_run"),
    ]

    operations = [
        migrations.AlterField(
            model_name="runhistogram",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="histograms",
                to="data_taking_objects.run",
            ),
        ),
    ]
