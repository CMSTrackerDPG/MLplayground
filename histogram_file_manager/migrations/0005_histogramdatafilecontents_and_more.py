# Generated by Django 4.1.3 on 2022-12-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('histogram_file_manager', '0004_alter_histogramdatafile_data_dimensionality_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistogramDataFileContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_dimensionality', models.PositiveIntegerField(blank=True, choices=[(1, '1D'), (2, '2D')], default=1)),
                ('granularity', models.CharField(choices=[('run', 'Run'), ('lum', 'Lumisection')], default='run', help_text='The granularity of the data contained in the data file (either whole run or lumisections).', max_length=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='histogramdatafile',
            name='data_dimensionality',
        ),
        migrations.RemoveField(
            model_name='histogramdatafile',
            name='granularity',
        ),
        migrations.AddField(
            model_name='histogramdatafile',
            name='contents',
            field=models.ManyToManyField(to='histogram_file_manager.histogramdatafilecontents'),
        ),
    ]
