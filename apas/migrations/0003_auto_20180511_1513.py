# Generated by Django 2.0.5 on 2018-05-11 12:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apas', '0002_auto_20180511_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rungtynes',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 11, 15, 13, 4, 789310)),
        ),
        migrations.AlterField(
            model_name='stavke',
            name='rungtynes',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rungtynes', to='apas.Rungtynes'),
        ),
    ]
