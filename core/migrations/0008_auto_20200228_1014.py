# Generated by Django 2.2.6 on 2020-02-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_dom_uruchomienie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dom',
            name='typ_budynku',
            field=models.CharField(default='', max_length=40),
        ),
    ]