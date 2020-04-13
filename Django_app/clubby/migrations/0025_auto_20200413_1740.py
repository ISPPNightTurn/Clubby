# Generated by Django 3.0.4 on 2020-04-13 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubby', '0024_auto_20200410_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, choices=[('rock', 'rock'), ('pop', 'pop'), ('techno', 'techno'), ('electro', 'electro'), ('hip hop', 'hip hop'), ('trap', 'trap'), ('reggaeton', 'reggaeton'), ('indie', 'indie'), ('metal', 'metal'), ('latin', 'latin'), ('edm', 'edm'), ('cumbia', 'cumbia'), ('rap', 'rap'), ('house', 'house'), ('r&b', 'r&b'), ('latino', 'latino'), ('dance', 'dance'), ('k-pop', 'k-pop'), ('funk', 'funk'), ('folk', 'folk'), ('disco', 'disco'), ('emo', 'emo'), ('country', 'country'), ('trance', 'trance'), ('reggae', 'reggae'), ('salsa', 'salsa'), ('soul', 'soul'), ('jazz', 'jazz'), ('ska', 'ska'), ('dubstep', 'dubstep'), ('rumba', 'rumba'), ('punk', 'punk'), ('ranchera', 'ranchera'), ('grunge', 'grunge'), ('flamenco', 'flamenco')], default='pop', help_text='event music type', max_length=100),
        ),
        migrations.AlterField(
            model_name='qr_item',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 13, 17, 40, 18, 330990)),
        ),
        migrations.AlterField(
            model_name='qr_item',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 13, 17, 40, 18, 330990)),
        ),
        migrations.AlterField(
            model_name='rating',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 13, 17, 40, 18, 327992)),
        ),
        migrations.AlterField(
            model_name='securityadvice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 13, 17, 40, 18, 328991)),
        ),
    ]