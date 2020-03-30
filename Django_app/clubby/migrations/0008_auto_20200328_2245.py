# Generated by Django 3.0.3 on 2020-03-28 21:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubby', '0007_auto_20200328_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, choices=[('r', 'refreshment'), ('c', 'cocktail'), ('s', 'shot'), ('b', 'beer'), ('w', 'wine'), ('k', 'snack'), ('h', 'hookah'), ('m', 'misc.')], default='m', help_text='product type', max_length=1),
        ),
        migrations.AlterField(
            model_name='qr_item',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 22, 45, 3, 919095)),
        ),
        migrations.AlterField(
            model_name='rating',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 22, 45, 3, 919095)),
        ),
    ]
