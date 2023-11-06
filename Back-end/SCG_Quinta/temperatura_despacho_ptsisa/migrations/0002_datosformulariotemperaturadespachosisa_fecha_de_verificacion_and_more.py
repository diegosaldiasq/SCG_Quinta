# Generated by Django 4.2.6 on 2023-11-06 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temperatura_despacho_ptsisa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosformulariotemperaturadespachosisa',
            name='fecha_de_verificacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datosformulariotemperaturadespachosisa',
            name='verificado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='datosformulariotemperaturadespachosisa',
            name='verificado_por',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]