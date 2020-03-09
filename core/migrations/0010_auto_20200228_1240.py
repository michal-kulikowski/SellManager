# Generated by Django 2.2.6 on 2020-02-28 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200228_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Konkurencja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_konkurencji', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='dom',
            name='konkurencja',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Lokale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer_mieszkania', models.IntegerField()),
                ('nasz_klient', models.BooleanField(default=False)),
                ('id_adr_dom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Dom', verbose_name='Dom')),
            ],
        ),
        migrations.AddField(
            model_name='dom',
            name='jaka_konkurencja',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Konkurencja'),
        ),
    ]