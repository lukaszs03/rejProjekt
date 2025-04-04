# Generated by Django 5.1.7 on 2025-03-24 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Realizacja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firma', models.CharField(max_length=255)),
                ('numer_rejestracyjny', models.CharField(max_length=20)),
                ('czynnosc', models.TextField()),
                ('data_dodania', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rejestrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=100)),
                ('nazwisko', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefon', models.CharField(max_length=20)),
            ],
        ),
    ]
