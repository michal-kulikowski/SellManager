# Generated by Django 2.2.6 on 2020-02-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_lokale_konkurencji_klient'),
    ]

    operations = [
        migrations.AddField(
            model_name='lokale',
            name='opis',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]