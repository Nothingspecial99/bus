# Generated by Django 5.1.1 on 2024-09-09 18:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_customuser_usertype'),
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
            field=models.ManyToManyField(to='main.bus'),
        ),
        migrations.AddField(
            model_name='record',
            name='recorder',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
