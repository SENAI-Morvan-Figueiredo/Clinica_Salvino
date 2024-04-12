# Generated by Django 5.0.4 on 2024-04-12 19:37

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('id_paciente', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('data_nascimento', models.DateField()),
                ('rg', models.CharField(max_length=9)),
                ('cpf', models.CharField(max_length=11)),
                ('status_dependencia', models.CharField(choices=[('Independente', 'Independente'), ('Dependente', 'Dependente')], max_length=20)),
                ('nome_responsavel', models.CharField(blank=True, max_length=256, null=True)),
                ('rg_responsavel', models.CharField(blank=True, max_length=9, null=True)),
                ('cpf_responsavel', models.CharField(blank=True, max_length=11, null=True)),
                ('telefone', models.CharField(max_length=14)),
                ('cep', models.CharField(max_length=8)),
                ('endereco', models.TextField()),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
