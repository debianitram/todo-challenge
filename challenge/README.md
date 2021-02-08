Desafío Invera
==============

### Requerimientos
- python3
- virtualenv (opcional virtualenwrapper)
- PostgreSQL (opcional).

## Instalación

1. Creación de un entorno virtual.
   
    ``` shell
   mkvirtualenv invera_todos --python=$(which python3)
   ```
2. Instalacion de dependencias: 
   
    ``` shell 
    pip install -r requiements/development.txt
    # Si utilizas PostgreSQL instalar desde el archivo: requirements/development_postgres.txt
   ```
3. Creacion de un usuario y una base de datos. (Preferentemente PostgreSQL)
   
    ``` postgres
        CREATE ROLE user_invera LOGIN PASSWORD 'inveraPassw0rd' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
        CREATE DATABASE db_invera_challenge WITH OWNER = user_invera;
    ```
4. Configuracion las variables de entorno para el proyecto desde `.env`
   ``` shell
        cp env.example .env
   ```
   
5. Correr migraciones: `python manage.py migrate`
6. Crear un usuario para probar desde la administración de django.
   ```shell
      python manage.py createsuperuser
   ```
7. Levantar servidor de desarrollo: `python manage.py runserver`


### Pruebas de integración.
Para correr la suite de tests ejecutar el comando: `pytest .`


### Acceso a la API.

List: 
   - `GET` /api/v1/todo/

Create: 
   - `POST` /api/v1/todo/  
     data: {"content": "Descripción de la tarea a crear"}

Delete: 
   - `DELETE` /api/v1/todo/{pk}/

Mark as completed: 
   - `POST` /api/v1/todo/mark_as_completed/
     data: {"tasks_id": [1, 2, 3]}

