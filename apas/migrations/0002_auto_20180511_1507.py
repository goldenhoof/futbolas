# Generated by Django 2.0.5 on 2018-05-11 12:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stavke',
            name='laimejimas',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rungtynes',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 11, 15, 7, 24, 516884)),
        ),
    ]
