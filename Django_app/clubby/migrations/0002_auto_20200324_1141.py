# Generated by Django 3.0.3 on 2020-03-24 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubby', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr_item',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 24, 11, 41, 16, 424077)),
        ),
        migrations.AlterField(
            model_name='rating',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 24, 11, 41, 16, 422970)),
        ),
    ]
