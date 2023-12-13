# SCG_Quinta
Desarrollo full developer web scg calidad quinta

## Abstracto

#### Este proyecto es para la transformacion digital del sistema de gestion de calidad, traspasando registros de papel que se iban a un registro muerto, transformandolo en una aplicacion web de alto rendimiento, inteligencia y respaldo de todo lo registrado en una base de datos.

## Como funciona esta aplicacion web

Para ingresar a la aplicacion es necesario un dispositivo movil, ya sea celular o tablet, con conexion a internet via wifi, estas seran usadas principalmente en areas productivas, en donde estan los datos a registrar. Se ingresa a la aplicacion web via una direccion (aun no definida) la cual nos llevara a una pagina web de toda la vida, pero esta es con la cromatica de quinta y con informacion que quinta necesita. Se debe crear un usuario, previa autorizacion del jefe de calidada o sub gerente de calidad, luego de esta autorizacion, quedara listo para poder ingrear los datos, se debe dirigir a "ingresar registros", luego le aparecera una lista de todos los registros, separados por planta o los que son formato en comun, se ingresa al seleccionado y se debe registrar cada vez que sea necesario, con los botones "grabar y continuar" para seguir ingresando datos en el mismo registro o si ya no se quiere ingrear mas datos de presiona "grabar y salir". Se debe hacer lo mismo con cada registro que se lleve, luego que se acabe su turno, debe cerrar secion y ya todos los datos que se regiistraron ya estan a salvo en la base de datos en el servidor (aun no definido). Luego estos datos seran analizados en la misma aplicacion o podran descargalos a su antojo para analizarlos via excel. 

## Herramientas y lenguajes de programacion utulizados

Se ha utilizado para el desarrollo frontend HTML, CSS y JavaScript. Para el desarrollo backend se utiliza Python con Django. La base de datos se quiere trabajar con PosgreSQL (aun por definir).
Se utiliza para el control de versiones y el manejor del flujo de trabajo git y github.

## Recursos necesarios para el proyecto

Para instalar el proyecto se debe tener instalado python 3.12.0, pip 23.2.1, django 4.2.6, docker 24.0.5, docker-compose 2.20.2, node 14.17.6, npm 10.1.0, git 2.39.2.

## Como ejecutar el proyecto

Iniciar sesion de docker con el comando `docker login` y luego ejecutar el comando `docker-compose up -d` para iniciar el servidor de desarrollo. Para bajar el servidor de desarrollo ejecutar el comando `docker-compose down`. Para ejecutar el servidor de desarrollo en modo interactivo ejecutar el comando `docker-compose up`. 

## Como ejecutar las pruebas

Para ejecutar las pruebas se debe tener instalado python 3.12.0, pip 23.2.1, django 4.2.6, docker 24.0.5, docker-compose 2.20.2, node 14.17.6, npm 10.1.0, git 2.39.2. Luego ejecutar el comando `docker-compose up -d` para iniciar el servidor de desarrollo. Luego ejecutar el comando `npm run test` para ejecutar las pruebas. Para bajar el servidor de desarrollo ejecutar el comando `docker-compose down`. Para ejecutar el servidor de desarrollo en modo interactivo ejecutar el comando `docker-compose up`.

## Como contribuir

Para contribuir se debe tener instalado git, clonar el repositorio de https://github.com/diegosaldiasq/SCG_Quinta, hacer tus modificaciones y luego debes hacer un pull request en github al proyecto https://github.com/diegosaldiasq/SCG_Quinta y esperar a que sea aprobado por el administrador del proyecto.