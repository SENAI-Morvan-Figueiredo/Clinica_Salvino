import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medico', '0001_initial'),
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_especialidade', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Tratamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=5)),
                ('descricao', models.TextField()),
            ],
        ),

        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('status_consulta', models.CharField(choices=[('Concluida', 'Concluida'), ('Cancelada', 'Cancelada'), ('Agendada', 'Agendada'), ('Em andamento', 'Em andamento')], max_length=256)),
                ('medico', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente')),
                ('especialidade', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clinica.especialidade')),
            ],
        ),
    ]
