# Generated by Django 3.1.2 on 2020-10-28 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20201025_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienteinfo',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clienteInfo', to='clients.cliente'),
        ),
    ]
