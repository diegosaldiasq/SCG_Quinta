from django.db import migrations


def seed(apps, schema_editor):
    Area = apps.get_model("productividad_turnos", "AreaProductividad")
    Area.objects.using(schema_editor.connection.alias).get_or_create(
        codigo="TORTAS", defaults={"nombre": "Tortas", "activo": True, "mide_semielaborado": True, "definicion_dotacion": "Personas presentes del área de Tortas durante el turno."}
    )


class Migration(migrations.Migration):
    dependencies = [("productividad_turnos", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]