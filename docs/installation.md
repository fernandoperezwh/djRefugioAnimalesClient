# Manual de instalación

- Elegir un directorio de fácil acceso para clonar el proyecto. 
    ```bash
    cd ~/Escritorio/
    ```
- Clonar el proyecto ya sea por ssh o https
    ```bash
    git clone git@github.com:fernandoperezwh/djRefugioAnimalesClient.git
    ```
    ```bash
    git clone https://github.com/fernandoperezwh/djRefugioAnimalesClient.git
    ```
- Crear un entorno virtual. Este proyecto fue elaborado en python 2.7 y por lo tanto debera crear el entorno con esta misma versión
    ```bash
    mkvirtualenv djRefugioAnimalesClient -p=2.7
    ```
- Activar el entorno creado en el anterior paso
    ```bash
    workon djRefugioAnimalesClient
    ```
- Instalar las dependencias del proyecto que se encuentran en el archivo `requirements.txt` 
    ```bash
    pip install -r requirements.txt
    ```
- Realizar las migraciones del proyecto 
    ```bash 
    python manage.py migrate
    ```
- Para comprobar que todo se encuentre correctamente, intente ejecutar el proyecto.
    ```bash
    python manage.py runserver
    ```
