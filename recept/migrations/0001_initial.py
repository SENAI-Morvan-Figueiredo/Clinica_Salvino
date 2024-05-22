# Generated by Django 5.0.4 on 2024-05-22 17:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recepcionista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('sexo', models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')], max_length=25)),
                ('genero', models.CharField(max_length=256)),
                ('data_nascimento', models.DateField()),
                ('rg', models.CharField(max_length=9, unique=True)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('telefone', models.CharField(max_length=14)),
                ('cep', models.CharField(max_length=8)),
                ('endereco', models.TextField()),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
