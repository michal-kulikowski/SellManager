# Generated by Django 2.2.6 on 2020-02-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200228_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lokale',
            name='klatka',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
