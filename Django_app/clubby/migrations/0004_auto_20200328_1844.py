# Generated by Django 3.0.3 on 2020-03-28 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubby', '0003_auto_20200328_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr_item',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 18, 44, 41, 183924)),
        ),
        migrations.AlterField(
            model_name='rating',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 18, 44, 41, 182925)),
        ),
    ]