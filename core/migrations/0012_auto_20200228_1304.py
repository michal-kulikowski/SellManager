# Generated by Django 2.2.6 on 2020-02-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200228_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lokale',
            name='data_modyfikacji',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]