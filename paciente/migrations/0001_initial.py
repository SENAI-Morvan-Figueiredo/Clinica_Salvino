# Generated by Django 5.0.4 on 2024-05-15 23:48

import django.db.models.deletion
import paciente.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinica', '0001_initial'),
        ('medico', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_consulta', models.CharField(choices=[('Presencial', 'Presencial'), ('Remoto', 'Remoto')], max_length=256)),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('status_consulta', models.CharField(choices=[('Concluida', 'Concluida'), ('Cancelada', 'Cancelada'), ('Agendada', 'Agendada'), ('Ficha Aberta', 'Ficha Aberta')], max_length=256)),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.especialidade')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
            ],
        ),
        migrations.CreateModel(
            name='AnexoConsulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to=paciente.models.anexo_paciente_upload)),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='paciente.consulta')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('sexo', models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')], max_length=25)),
                ('genero', models.CharField(max_length=256)),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente'),
        ),
        migrations.CreateModel(
            name='CadConvenio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_carteirinha', models.CharField(max_length=256)),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.convenio')),
                ('plano_convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.planoconvenio')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente')),
            ],
            options={
                'verbose_name_plural': 'CadConvenio',
            },
        ),
        migrations.CreateModel(
            name='CadCartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cartao', models.CharField(max_length=256)),
                ('cvc', models.CharField(max_length=3)),
                ('data_vencimento', models.CharField(max_length=7)),
                ('bandeira_cartao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.bandeiracartao')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente')),
            ],
            options={
                'verbose_name_plural': 'CadCartao',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_emissao', models.DateField()),
                ('forma_pagamento', models.CharField(choices=[('Convenio', 'Convenio'), ('Cartao', 'Cartao'), ('Pix', 'Pix'), ('Boleto', 'Boleto'), ('Pagar no dia', 'Pagar no dia')], max_length=256)),
                ('boleto', models.FileField(blank=True, null=True, upload_to='boletos/')),
                ('cod_barras', models.CharField(blank=True, max_length=44, null=True)),
                ('status_pagamento', models.CharField(choices=[('Pago', 'Pago'), ('Aguardando pagamento', 'Aguardando pagamento'), ('Cancelado', 'Cancelado'), ('Aguardando reembolso', 'Aguardando reembolso'), ('Reembolsado', 'Reembolsado')], max_length=256)),
                ('data_pagamento', models.CharField(blank=True, max_length=256, null=True)),
                ('cartao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='paciente.cadcartao')),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.consulta')),
                ('convenio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='paciente.cadconvenio')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente')),
                ('pix', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinica.pix')),
                ('tratamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.tratamento')),
            ],
        ),
        migrations.CreateModel(
            name='Prontuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=3)),
                ('alergia', models.BooleanField()),
                ('doenca', models.BooleanField()),
                ('fuma', models.BooleanField()),
                ('bebe', models.BooleanField()),
                ('uso_drogas', models.BooleanField()),
                ('observacoes', models.TextField(null=True)),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Encaminhamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('tipo_encaminhamento', models.CharField(choices=[('Consultas', 'Consultas'), ('Exames e Terapias', 'Exames e Terapias'), ('Outros', 'Outros')], max_length=256)),
                ('area', models.CharField(max_length=256)),
                ('descricao', models.TextField(null=True)),
                ('file_documento', models.FileField(upload_to='anexo_medico_upload')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
                ('prontuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.prontuario')),
            ],
            options={
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_documento', models.CharField(max_length=256)),
                ('tipo_documento', models.CharField(choices=[('Descrição de Atendimento', 'Descrição de Atendimento'), ('Receita', 'Receita'), ('Dieta', 'Dieta')], max_length=256)),
                ('data', models.DateField()),
                ('descricao', models.TextField(null=True)),
                ('file_documento', models.FileField(blank=True, null=True, upload_to=paciente.models.anexo_medico_upload)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
                ('prontuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.prontuario')),
            ],
            options={
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.CreateModel(
            name='Bioimpedância',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=3)),
                ('massa_magra', models.DecimalField(decimal_places=2, max_digits=5)),
                ('massa_muscular', models.DecimalField(decimal_places=2, max_digits=5)),
                ('agua_corporal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('densidade_ossea', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gordura_visceral', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gordura_corporal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('taxa_metabolica', models.DecimalField(decimal_places=2, max_digits=5)),
                ('imc', models.DecimalField(decimal_places=2, max_digits=4)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
                ('prontuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.prontuario')),
            ],
            options={
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.AddConstraint(
            model_name='cadconvenio',
            constraint=models.UniqueConstraint(fields=('convenio', 'plano_convenio'), name='unique_convenio_plano_convenio'),
        ),
    ]
