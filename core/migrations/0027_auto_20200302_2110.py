# Generated by Django 2.2.6 on 2020-03-02 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_ulotki'),
    ]

    operations = [
        migrations.AddField(
            model_name='ulotki',
            name='ilosc',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='telefon',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
