# Generated by Django 2.2.6 on 2020-02-28 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_dom_uruchomienie'),
    ]

    operations = [
        migrations.AddField(
            model_name='dom',
            name='uruchomienie',
            field=models.DateField(null=True),
        ),
    ]