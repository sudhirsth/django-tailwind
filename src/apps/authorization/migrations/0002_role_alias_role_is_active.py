# Generated by Django 4.1.9 on 2023-07-03 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='alias',
            field=models.CharField(default=models.CharField(max_length=100), max_length=100),
        ),
        migrations.AddField(
            model_name='role',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]