# Generated by Django 5.1.1 on 2024-09-09 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_record_bus_remove_record_recorder_record_bus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='bus',
        ),
        migrations.RemoveField(
            model_name='record',
            name='recorder',
        ),
        migrations.AddField(
            model_name='record',
            name='bus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.bus'),
        ),
        migrations.AddField(
            model_name='record',
            name='recorder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
