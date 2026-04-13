from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trazabilidad_productos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrotrazabilidad',
            name='acciones_correctivas_requieren_revision',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registrotrazabilidad',
            name='acciones_correctivas_verificadas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registrotrazabilidad',
            name='fecha_verificacion_acciones',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrotrazabilidad',
            name='nombre_verificador_acciones',
            field=models.CharField(max_length=150, blank=True, null=True),
        ),
    ]