# Implementación
El registro solicita unidades elaboradas (entero mayor que cero). Los registros anteriores conservan NULL y aparecen como «Sin registro».
El historial filtra un rango inclusivo de fechas de elaboración del producto; Excel usa los mismos filtros explícitos.

## Base de datos
Este repositorio no incluye las migraciones existentes de trazabilidad_productos. Genere la nueva migración en el entorno que conserva las migraciones aplicadas, después de copiar models.py:
```bash
python manage.py makemigrations trazabilidad_productos
python manage.py migrate trazabilidad_productos
```
Si usa Docker, ejecute ambos comandos dentro del contenedor Django.
La nueva migración debe agregar únicamente unidades_elaboradas a RegistroTrazabilidad. Si makemigrations propone crear las tablas existentes, deténgase y restaure primero las migraciones originales del servidor.
Aplique la migración antes de reiniciar el servicio web con el código actualizado.

## Verificación
Registrar un producto con una cantidad positiva, comprobarla en historial y Excel.
Comprobar rechazo de vacío, cero, negativos y decimales.
Consultar dos fechas de elaboración distintas y verificar que ambos extremos aparezcan.
Comprobar rechazo de un rango invertido y conservación del rango al paginar.

