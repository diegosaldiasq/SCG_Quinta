# SCG_Quinta
Desarrollo full developer web scg calidad quinta

## Abstracto

#### Este proyecto es para la transformacion digital del sistema de gestion de calidad, traspasando registros de papel que se iban a un registro muerto, transformandolo en una aplicacion web de alto rendimiento, inteligencia y respaldo de todo lo registrado en una base de datos.

## Como funciona esta aplicacion web

Para ingresar a la aplicacion es necesario un dispositivo movil, ya sea celular o tablet, con conexion a internet via wifi, estas seran usadas principalmente en areas productivas, en donde estan los datos a registrar. Se ingresa a la aplicacion web via una direccion (aun no definida) la cual nos llevara a una pagina web de toda la vida, pero esta es con la cromatica de quinta y con informacion que quinta necesita. Se debe crear un usuario, previa autorizacion del jefe de calidada o sub gerente de calidad, luego de esta autorizacion, quedara listo para poder ingrear los datos, se debe dirigir a "ingresar registros", luego le aparecera una lista de todos los registros, separados por planta o los que son formato en comun, se ingresa al seleccionado y se debe registrar cada vez que sea necesario, con los botones "grabar y continuar" para seguir ingresando datos en el mismo registro o si ya no se quiere ingrear mas datos de presiona "grabar y salir". Se debe hacer lo mismo con cada registro que se lleve, luego que se acabe su turno, debe cerrar secion y ya todos los datos que se regiistraron ya estan a salvo en la base de datos en el servidor (aun no definido). Luego estos datos seran analizados en la misma aplicacion o podran descargalos a su antojo para analizarlos via excel. 

## Herramientas y lenguajes de programacion utulizados

Se ha utilizado para el desarrollo frontend HTML, CSS y JavaScript. Para el desarrollo backend se utiliza el framework de Python para aplicaciones web Django. La base de datos esta construida con PosgreSQL. EL servidor para uso proxy inverso se usa Nginx. Toda la aplicacion se conteneriza en 4 contenedores con la ayuda de `Docker` y `docker-compose`. El primero es de la aplicacion web, nombre contenedor `web`, donde se encuentra todo el codigo de la aplicacion y los archivos static. El segundo contenedores para la base de datos de postgres, nombre contenedor `db`, donde esta la logica de control para las tablas de la base, esta depende para el funcionamiento `web`. El tercer contenedor es para la adminstracion de `db` lo cual se usa `pgadmin4`, con el nombre de contenedor `pgadmin`, el cual depende de `db`. El cuarto contenedor es para el servidor de proxy inverso el cual funciona con `nginx`, con el nombre de `nginx`, este depende de `web`. Asi se conforma la arquitectura de contenedores de `docker-compose`.
Se utiliza para el control de versiones y el manejor del flujo de trabajo git y github en el link https://github.com/diegosaldiasq/SCG_Quinta

## Recursos necesarios para el proyecto

Para instalar el proyecto se debe tener instalado python 3.12.0, pip 23.2.1, django 4.2.6, docker 24.0.5, docker-compose 2.20.2, node 14.17.6, npm 10.1.0, git 2.39.2. Esto es informativo ya que cuando se corre la instalacion de los contenedores, al crear el contenedor de web, se creara junto con los requerimietos alojados en el archivo `requirements.txt`. Destallada su su instalacion en `Dockerfile`.

## Como ejecutar el proyecto

### Comandos necesarios para Django
##### Clonar el repositorio de Github
Para tener el proyecto en tu maquina local o servidor de produccion, se debe clonar el repositorio de `Github`. Se debe tener `Git` instalado en la maquina donde se quiere clonar el repositorrio, luego correr el siguiente comando `git clone https://github.com/diegosaldiasq/SCG_Quinta` esto descargara todo lo necesario para correr el proyecto con los siguientes comando.
##### Para agregar llave publica de Github (Uso Diego Saldias)
ssh-keygen -t rsa -b 4096 -C "diego.saldias.quijada@gmail.com" - para generar la llave publica y privada
eval $(ssh-agent -s) - para iniciar el agente ssh (para windows)
eval "$(ssh-agent -s)" - para iniciar el agente ssh (para linux)
ssh-add ~/.ssh/id_rsa - para agregar la llave privada al agente ssh
##### Comandos GIT
git push origin main - para subir los cambios al repositorio de github
git pull origin main - para bajar los cambios del repositorio de github
git add * - para agregar todos los cambios al repositorio local, menos lo de gitignore
git commit -m "mensaje" - para hacer un commit con un mensaje
git commit -am "mensaje" - para agregar y hacer commit al mismo tiempo
git status - para ver el estado de los archivos en el repositorio local
##### Entorno virtual
Iniciar el entorno virtual en la carpeta `Back-end` (para linux) `source venv/bin/activate`, (para windows) `source venv/Scripts/activate`. Para salir del ambiente vistual se debe correr el comando `deactivate`.
##### Migraciones
Correr en django el comando `python manage.py makemigrations`, si es necesario correrlo con el sufijo de cada `app` para migrar las tablas a la base de datos. Luego corerr el comando `python manage.py migrate` para hacer efectivo los cambios.
##### Aplicaciones
Para crear un aplicacion debe estar activo el entorno virtual y funcionando, luego se debe correr el comando `python manage.py startapp nombre_app`, esto creara una nueva carpeta con el nombre de la aplicacion y los archivos necesarios para su funcionamiento. Luego se debe agregar la aplicacion en el archivo `settings.py` en la lista de `INSTALLED_APPS`.
##### Superusuario
Con el entorno activo y funcionando, se puede correr el comando de django `python manage.py createsuperuser` y seguir las instrucciones de creacion de superusuario.
##### Para cambios en archivos static
Para hacer efectivos en el srevidor los cambios hechos a cualquier archivo que se encuentre en la carpeta `static`, se debe correr el comando de django `python manage.py collectstatic` para hacer efectivos los cambios en el servidor antes de correr los contenedores.

### Comandos necesarios para Docker

docker login - Para conectarse con Docker Hub
docker-compose up -d --build - Para construir las imagenes e iniciar los contenedores
docker-compose up -d - Para iniciar los contenedores
docker-compose down - Para terminar con los contenedores

Iniciar sesion de docker (se debebe tener Docker instalado) con el comando `docker login` y luego ejecutar el comando `docker-compose up -d` para iniciar el servidor de desarrollo. Para bajar el servidor de desarrollo ejecutar el comando `docker-compose down`. Para ejecutar el servidor de desarrollo en modo interactivo ejecutar el comando `docker-compose up`. 

## PGAdmin de postgres

Para el acceso local se debe ingreaar a http://localhost:5050 e ingresar con usuario y contraseña.

## Como ejecutar las pruebas

Para ejecutar las pruebas se debe tener instalado python 3.12.0, pip 23.2.1, django 4.2.6, docker 24.0.5, docker-compose 2.20.2, node 14.17.6, npm 10.1.0, git 2.39.2. Luego ejecutar el comando `docker-compose up -d` para iniciar el servidor de desarrollo. Luego ejecutar el comando `npm run test` para ejecutar las pruebas. Para bajar el servidor de desarrollo ejecutar el comando `docker-compose down`. Para ejecutar el servidor de desarrollo en modo interactivo ejecutar el comando `docker-compose up`.

## Para arrancar en AWS

Conectar al contenedor `db` con el comando `docker-compose exec web python manage.py makemigrations` para crear las migraciones de la base de datos. Luego correr el comando `docker-compose exec web python manage.py migrate` para aplicar las migraciones a la base de datos. Luego correr el comando `docker-compose exec web python manage.py collectstatic` para recolectar los archivos static y hacerlos efectivos en el servidor. Crear el superusuario con `docker-compose exec web python manage.py createsuperuser` y seguir las instrucciones de creacion de superusuario.

## Como contribuir

Para contribuir se debe tener instalado git, clonar el repositorio de https://github.com/diegosaldiasq/SCG_Quinta, hacer tus modificaciones y luego debes hacer un pull request en github al proyecto https://github.com/diegosaldiasq/SCG_Quinta y esperar a que sea aprobado por el administrador del proyecto.

## Licencia

Licencia MIT

Copyright (c) [2023] [Diego Saldías Quijada]

Por el presente se otorga permiso, sin cargo, a cualquier persona que obtenga una copia de este software y los archivos de documentación asociados (el "Software"), para operar con el Software sin restricciones, incluidos, entre otros, los derechos de uso, copia, modificación, fusión. , publicar, distribuir, sublicenciar y/o vender copias del Software, y permitir que las personas a quienes se les proporciona el Software lo hagan, sujeto a las siguientes condiciones:

El aviso de derechos de autor anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A LAS GARANTÍAS DE COMERCIABILIDAD, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DE DERECHOS DE AUTOR SERÁN RESPONSABLES DE NINGÚN RECLAMO, DAÑO U OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE OTRA MANERA, QUE SURJA DE, FUERA DE O EN RELACIÓN CON EL SOFTWARE O EL USO U OTRAS NEGOCIOS EN EL SOFTWARE.