# Generated by Django 3.1.2 on 2020-11-08 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20201028_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
