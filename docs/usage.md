# Manual de uso

Este proyecto surge como aplicación cliente para probar los tres tipos de autentificación: 
[Token Authentication](https://github.com/fernandoperezwh/djRefugioAnimalesTokenAuthAPI), 
[JSON Web Token Authentication](https://github.com/fernandoperezwh/djRefugioAnimalesSimpleJwtAPI) y 
[OAuth 2.0](https://github.com/fernandoperezwh/djRefugioAnimalesOAuthAPI). 
Por lo tanto, puede configurar que tipo de autentificación utilizar desde un archivo `.env.<PYTHON_ENV>`

## Respecto a los archivos .env
En el proyecto se encuentra el directorio `.environments` el cual contiene los archivos `.env.<PYTHON_ENV>` que,
dependiendo del entorno definido en la variable `PYTHON_ENV`, se usarán para cargar en el runtime las variables 
de entorno. 

Por ejemplo para un ambiente de _"desarrollo"_ la variable _PYTHON_ENV_ debe estar definida como _"development"_ 
o en representación`PYTHON_ENV=development`. En este escenario, el archivo que usaria el settings para nuestro 
proyecto seria el archivo `.environments/.env.development`.


## Descripción de los archivos .env
El archivo `.env` sirve como base de los archivos `.env.<PYTHON_ENV>` ya que contiene las variables que deben estar presentes.

| variable                         | Descripción                                                                                                                                           | Default              |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| `DEBUG=`                         | Define si la aplicación corre en modo debug                                                                                                           | false                |
| `SECRET_KEY=`                    | Django secret key                                                                                                                                     |                      |
| `DJREFUGIOANIMALES_API_SERVER=`  | Define la API de Refugio de Animales con la cual se trabajara. <br/><br/>Las opciones validas son: "token_auth_server", "jwt_server" y "oauth_server" | 'token_auth_server'  |


### Datos de configuración para autentificación

#### Token Authentication
Para trabajar con la API de Refugio de Animales que utiliza este tipo de autentificación, debe asegurarse de que 
en archivo __.env.<PYTHON_ENV>__ se encuentre la variable `DJREFUGIOANIMALES_API_SERVER` definida como `token_auth_server`
```
DJREFUGIOANIMALES_API_SERVER=token_auth_server
```

A continuación asegúrese de definir las siguientes variables para la conexión con el servidor.

| variable                                    | Descripción                                          | Default          |
|---------------------------------------------|------------------------------------------------------|------------------|
| `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_HOST=` | Host del servidor de la API de Refugio de Animales   | http://127.0.0.1 |
| `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_PORT=` | Puerto del servidor de la API de Refugio de Animales | 8010             |


Finalmente defina las credenciales de autentificación que usarán.

| variable                                                       | Descripción                                                                                                                                                                          | Default |
|----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_USERNAME=`                | Username para realizar la autentificación y obtener el access_token haciendo uso también del 'password'                                                                              |         |
| `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_PASSWORD=`                | Password para realizar la autentificación y obtener el access_token haciendo uso también del 'username'                                                                              |         |
| `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_ACCESS_TOKEN=`            | Token de acceso del usuario.<br/><br/> Cuando se especifica un access_token valido este se usara directamente sin pasar por el endpoint para generar token                           |         |
| `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_TRY_AUTH_IN_TOKEN_FAIL=`  | Indica si se utiliza el 'username' y 'password' para solicitar un nuevo token de acceso cuando el token definido en `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_ACCESS_TOKEN=` es invalido. | false   |

> __Para obtener su "access_token" puede seguir el siguiente [manual](https://github.com/fernandoperezwh/djRefugioAnimalesTokenAuthAPI/blob/master/docs/usage.md#obtener-token-mediante-la-interfaz-de-la-aplicación)__



#### JSON Web Token Authentication
Para trabajar con la API de Refugio de Animales que utiliza este tipo de autentificación, debe asegurarse de que 
en archivo __.env.<PYTHON_ENV>__ se encuentre la variable `DJREFUGIOANIMALES_API_SERVER` definida como `jwt_server`
```
DJREFUGIOANIMALES_API_SERVER=jwt_server
```
A continuación asegúrese de definir las siguientes variables para la conexión con el servidor.

| variable                             | Descripción                                          | Default          |
|--------------------------------------|------------------------------------------------------|------------------|
| `DJREFUGIOANIMALES_SERVER_JWT_HOST=` | Host del servidor de la API de Refugio de Animales   | http://127.0.0.1 |
| `DJREFUGIOANIMALES_SERVER_JWT_PORT=` | Puerto del servidor de la API de Refugio de Animales | 8011             |

Finalmente defina las credenciales de autentificación que usarán.

| variable                                               | Descripción                                                                                                                                                                                                      | Default |
|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `DJREFUGIOANIMALES_SERVER_JWT_USERNAME=`               | Username para realizar la autentificación y obtener el access_token haciendo uso también del 'password'                                                                                                          |         |
| `DJREFUGIOANIMALES_SERVER_JWT_PASSWORD=`               | Password para realizar la autentificación y obtener el access_token haciendo uso también del 'username'                                                                                                          |         |
| `DJREFUGIOANIMALES_SERVER_JWT_ACCESS_TOKEN=`           | Token de acceso del usuario.<br/><br/> Cuando se especifica un access_token valido este se usara directamente sin pasar por el endpoint para generar token                                                       |         |
| `DJREFUGIOANIMALES_SERVER_JWT_REFRESH_TOKEN=`          | Token para hacer refresh del token de acceso.<br/><br/> Cuando se especifica un access_token valido este se usara directamente para solicitar un nuevo access_token sin pasar por el endpoint para generar token |         |
| `DJREFUGIOANIMALES_SERVER_JWT_TRY_AUTH_IN_TOKEN_FAIL=` | Indica si se utiliza el 'username' y 'password' para solicitar un nuevo token de acceso cuando el token definido en `DJREFUGIOANIMALES_SERVER_TOKEN_AUTH_ACCESS_TOKEN=` es invalido.                             | false   |

> __Para obtener su "access_token" y "refresh_token" puede seguir el siguiente [manual](https://github.com/fernandoperezwh/djRefugioAnimalesSimpleJwtAPI/blob/master/docs/usage.md#obtener-access_token-y-refresh_token-mediante-la-interfaz-de-la-aplicación)__





#### OAuth2.0
Para trabajar con la API de Refugio de Animales que utiliza este tipo de autentificación, debe asegurarse de que 
en archivo __.env.<PYTHON_ENV>__ se encuentre la variable `DJREFUGIOANIMALES_API_SERVER` definida como `oauth_server`
```
DJREFUGIOANIMALES_API_SERVER=oauth_server
```


A continuación asegúrese de definir las siguientes variables para la conexión con el servidor.

| variable                               | Descripción                                          | Default          |
|----------------------------------------|------------------------------------------------------|------------------|
| `DJREFUGIOANIMALES_SERVER_OAUTH_HOST=` | Host del servidor de la API de Refugio de Animales   | http://127.0.0.1 |
| `DJREFUGIOANIMALES_SERVER_OAUTH_PORT=` | Puerto del servidor de la API de Refugio de Animales | 8012             |


Finalmente defina las credenciales de autentificación que usarán.

| variable                                        | Descripción                                                                |
|-------------------------------------------------|----------------------------------------------------------------------------|
| `DJREFUGIOANIMALES_SERVER_OAUTH_CLIENT_ID=`     | Client id de la aplicación registrada para realizar la autentificación     |
| `DJREFUGIOANIMALES_SERVER_OAUTH_CLIENT_SECRET=` | Client secret de la aplicación registrada para realizar la autentificación |

> __Para obtener su "client_id" y "client_secret" puede seguir el siguiente [manual]()__

