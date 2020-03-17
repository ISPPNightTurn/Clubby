# Generated by Django 3.0.3 on 2020-03-11 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubby', '0011_auto_20200311_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='start_time',
        ),
        migrations.AddField(
            model_name='reservation',
            name='max_time',
            field=models.IntegerField(default=4, help_text='max hours after the event starts people can arrive at.', max_length=2),
        ),
    ]
