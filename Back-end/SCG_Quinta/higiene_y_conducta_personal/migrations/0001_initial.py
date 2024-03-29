# Generated by Django 4.2.4 on 2023-08-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosFormularioHigieneConductaPersonal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateTimeField()),
                ('nombre_personal', models.CharField(max_length=100)),
                ('turno', models.TextField()),
                ('planta', models.TextField()),
                ('area', models.TextField()),
                ('cumplimiento', models.TextField()),
                ('desviacion', models.TextField()),
                ('accion_correctiva', models.TextField()),
                ('verificacion_accion_correctiva', models.TextField()),
                ('observacion', models.TextField()),
                ('nombre_tecnologo', models.CharField(max_length=100)),
            ],
        ),
    ]
