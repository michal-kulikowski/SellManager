# Generated by Django 2.2.6 on 2020-03-07 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20200307_1116'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RodzajKontaktu',
        ),
        migrations.RemoveField(
            model_name='lokale',
            name='rodzaj_kontaktu',
        ),
        migrations.RemoveField(
            model_name='lokalehistory',
            name='rodzaj_kontaktu',
        ),
    ]