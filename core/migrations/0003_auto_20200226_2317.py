# Generated by Django 2.2.6 on 2020-02-26 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200226_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dom',
            name='miejscowosc',
            field=models.CharField(default='', max_length=100),
        ),
    ]
