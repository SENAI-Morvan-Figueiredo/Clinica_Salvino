# Generated by Django 5.0.4 on 2024-05-16 19:47

import paciente.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encaminhamento',
            name='file_documento',
            field=models.FileField(upload_to=paciente.models.anexo_medico_upload),
        ),
    ]