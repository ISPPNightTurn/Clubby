# Generated by Django 3.0.3 on 2020-05-07 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubby', '0032_auto_20200507_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr_item',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 16, 26, 16, 734324)),
        ),
        migrations.AlterField(
            model_name='qr_item',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 16, 26, 16, 734324)),
        ),
        migrations.AlterField(
            model_name='rating',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 16, 26, 16, 733330)),
        ),
        migrations.AlterField(
            model_name='securityadvice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 16, 26, 16, 733330)),
        ),
    ]