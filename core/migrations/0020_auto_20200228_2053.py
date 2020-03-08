# Generated by Django 2.2.6 on 2020-02-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200228_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lokale',
            name='data_dodania_wpisu',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='data_kolejnego_kontaktu',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='data_konca_umowy',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='data_kontaktu',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='data_modyfikacji',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='klatka',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Obecnie płaci'),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='rodzaj_kontaktu',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
