# Generated by Django 3.0.3 on 2020-03-12 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubby', '0013_auto_20200311_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='date',
        ),
        migrations.AddField(
            model_name='ticket',
            name='category',
            field=models.CharField(default='Basic', help_text='The name of the type of ticket you are trying to sell.', max_length=40),
        ),
        migrations.AddField(
            model_name='ticket',
            name='description',
            field=models.TextField(default='this allows you to enter the party.', help_text='Decribe what this ticket entices.'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]