# Generated by Django 2.2.6 on 2020-02-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200228_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lokale',
            name='rodzaj_kontaktu',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='uzytkownik',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
