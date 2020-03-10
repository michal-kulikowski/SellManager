# Generated by Django 2.2.6 on 2020-03-09 20:10

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0035_auto_20200307_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instalacje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poprzedni_numer_klienta', models.CharField(max_length=50)),
                ('numer_klienta', models.IntegerField()),
                ('data_instalacji', models.DateTimeField(auto_now_add=True)),
                ('notatka', models.CharField(max_length=200)),
                ('uzytkownik', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InstalacjeZdjecia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default=None, upload_to='Instalacje/%Y/%m/%d', validators=[core.models.my_validate])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('instalacje', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Instalacje')),
            ],
        ),
    ]
