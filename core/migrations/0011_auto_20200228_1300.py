# Generated by Django 2.2.6 on 2020-02-28 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200228_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='lokale',
            name='data_dodania_wpisu',
            field=models.DateField(auto_created=True, null=True),
        ),
        migrations.AddField(
            model_name='lokale',
            name='data_kolejnego_kontaktu',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='lokale',
            name='data_konca_umowy',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='lokale',
            name='data_kontaktu',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='lokale',
            name='data_modyfikacji',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lokale',
            name='klatka',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='lokale',
            name='konkurencja',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Konkurencja'),
        ),
        migrations.AddField(
            model_name='lokale',
            name='rodzaj_kontaktu',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lokale',
            name='uzytkownik',
            field=models.CharField(default='', max_length=50),
        ),
    ]