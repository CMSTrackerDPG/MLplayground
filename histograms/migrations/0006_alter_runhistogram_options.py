# Generated by Django 3.2.8 on 2022-05-05 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("histograms", "0005_auto_20220429_0949"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="runhistogram",
            options={"ordering": ["title"]},
        ),
    ]