# Generated by Django 3.1.2 on 2020-10-20 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20201020_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='hora',
        ),
    ]
