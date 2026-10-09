# Cálculo automático y revisión de OEE

El registro completo de un turno y el cierre de producción real llaman al mismo servicio de cálculo. Los datos coherentes generan el resumen automáticamente, sin marcarlo como verificado. Los registros inconsistentes permanecen sin resumen y se muestran en **Requiere revisión / pendiente**, con sus motivos. El enlace anterior `estado=calcular_oee` sigue funcionando.

La pantalla **Revisar OEE** permite a usuarios `is_staff` o superusuarios corregir datos del turno, cantidades por producto, horarios de detenciones y reprocesos. Los demás usuarios pueden consultar los motivos. Al guardar, se reevalúa el turno; si es válido, se crea el resumen y desaparece del listado de pendientes. Las tasas nominales deben corregirse en el catálogo correspondiente al área y supervisor.

## Validaciones

- Tiempo planeado y personas mayores que cero; producción planeada completa.
- Producción real por producto completa, incluyendo ceros explícitos, y totales coherentes.
- Tasas nominales existentes, positivas y finitas; sin valores nominales de 80 por defecto.
- Paros no superiores al tiempo planeado; horarios y duraciones coincidentes; detenciones no superpuestas, incluido el cruce de medianoche.
- Reprocesos no superiores a la producción real; producción incompatible con tiempo operativo cero.
- Rendimiento máximo inicial de 100 % y OEE no superior al 100 %.
- Un OEE bajo o igual a cero no genera una alerta por sí mismo.

El límite del rendimiento puede configurarse en settings como `OEE_RENDIMIENTO_MAXIMO = 110`, si se valida esa tolerancia internamente. Un OEE superior al 100 % sigue quedando en revisión.

## Fórmula y compatibilidad

Se conserva la unidad actual de `un_pp`: unidades por persona por turno. No se transforma en tasa por hora ni se cambia la base temporal del cálculo existente. Para un producto: producción teórica = un_pp × personas; rendimiento = producción real / teórica; OEE = disponibilidad × rendimiento × calidad.

Para varios productos se usa una media armónica ponderada por cantidades reales: tasa equivalente = suma(unidades) / suma(unidades/tasa). Si no hubo producción, se utiliza la mezcla planeada. Esto evita que un promedio simple ignore las proporciones de productos con distintas capacidades. La cantidad teórica se redondea para almacenarla, pero el indicador se calcula con el valor sin redondear.

Los resúmenes históricos y sus verificaciones humanas se conservan; este cambio no los audita ni recalcula. Un turno que ya tiene resumen no se vuelve a cerrar o modificar desde las pantallas nuevas. El servicio bloquea el turno durante el cálculo para evitar resúmenes duplicados en llamadas concurrentes sobre PostgreSQL.

## Activación

1. Aplicar los archivos modificados o el parche y actualizar/recrear el contenedor web con el procedimiento habitual.
2. No se agregan campos ni tablas: este cambio no requiere migraciones de base de datos.
3. Como administrador, entrar al listado de turnos y pulsar **Calcular automáticamente los turnos pendientes**. Procesa todos los pendientes con producción real, independientemente de los filtros visibles. Solo crea resúmenes para los válidos.
4. Seleccionar **Requiere revisión / pendiente** para corregir los restantes.

También se pueden procesar los pendientes desde el directorio de `manage.py`:

```bash
python manage.py procesar_oee_pendientes
```

En Docker, ejecutar ese comando dentro del contenedor de Django.

## Pruebas

```bash
python manage.py test calculo_oee --settings=calculo_oee.test_settings
```

La configuración aislada utiliza SQLite en memoria y el usuario personalizado del proyecto. No utiliza credenciales ni accede a la base de producción. Cubre cálculo, validaciones, mezcla de productos, medianoche, cierre, alta completa, pendientes, permisos y edición. La semántica de bloqueo concurrente de PostgreSQL no se prueba con SQLite.