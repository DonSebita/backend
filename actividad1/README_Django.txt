README - GUIA PERSONAL PARA APRENDER DJANGO
================================================

OBJETIVO
--------
Este archivo es una guia personal para entender Django de verdad, no solo
memorizar codigo.

La idea es poder mirar cualquier proyecto Django y entender:

    navegador
        |
        v
    URL
        |
        v
    VIEW
        |
        +----> MODEL / ORM ----> BASE DE DATOS
        |
        v
    TEMPLATE
        |
        v
    RESPONSE
        |
        v
    navegador

En nuestros proyectos hemos trabajado especialmente con:

- Proyecto y apps.
- urls.py y path().
- include().
- Views.
- Models.
- ORM.
- Migraciones.
- Templates.
- Herencia de templates.
- Contexto.
- Formularios HTML.
- GET y POST.
- CSRF.
- CRUD.
- get_object_or_404().
- redirect().
- Static y CSS.
- Template tags.
- Configuracion generica para reutilizar vistas.
- Git y estructura de Django.
- Django REST Framework (DRF).
- APIs y JSON.
- Errores comunes como 404, TemplateDoesNotExist y NoReverseMatch.


================================================================
1. QUE ES DJANGO
================================================================

Django es un framework web escrito en Python.

Un framework proporciona una estructura y herramientas para crear aplicaciones
web.

Sin Django tendriamos que implementar muchas cosas manualmente:

- Recibir peticiones HTTP.
- Enrutar URLs.
- Trabajar con bases de datos.
- Validar formularios.
- Manejar sesiones.
- Autenticacion.
- Proteccion CSRF.
- Renderizado de HTML.
- Administracion.
- APIs, si utilizamos DRF.

Django nos da estas herramientas ya preparadas.


================================================================
2. PROYECTO VS APP
================================================================

Esta diferencia es fundamental.

PROYECTO
--------

El proyecto es el contenedor general.

Ejemplo:

    mi_proyecto/
    |
    +-- manage.py
    |
    +-- mi_proyecto/
        +-- settings.py
        +-- urls.py
        +-- asgi.py
        +-- wsgi.py

La carpeta interna mi_proyecto contiene la configuracion principal.

APP
---

Una app es una parte funcional del proyecto.

Por ejemplo:

    mi_proyecto/
    |
    +-- biblioteca/
    |
    +-- estudiantes/
    |
    +-- api/

Cada app puede encargarse de una funcionalidad diferente.

Ejemplo:

    biblioteca
        -> libros
        -> autores
        -> lectores
        -> prestamos

    estudiantes
        -> estudiantes
        -> salones
        -> clases

Una app NO tiene que ser necesariamente una sola tabla.
La idea es agrupar funcionalidad relacionada.


================================================================
3. manage.py
================================================================

manage.py es el archivo que utilizamos para ejecutar comandos de Django.

Ejemplos:

    python manage.py runserver

Inicia el servidor de desarrollo.

    python manage.py startapp biblioteca

Crea una app.

    python manage.py makemigrations

Detecta cambios en los modelos y prepara migraciones.

    python manage.py migrate

Aplica las migraciones a la base de datos.

    python manage.py createsuperuser

Crea un usuario administrador.

    python manage.py shell

Abre una consola Python con Django configurado.


================================================================
4. settings.py
================================================================

settings.py contiene la configuracion principal.

Entre otras cosas:

    INSTALLED_APPS
    MIDDLEWARE
    ROOT_URLCONF
    TEMPLATES
    DATABASES
    STATIC_URL
    STATICFILES_DIRS
    SECRET_KEY
    DEBUG
    ALLOWED_HOSTS

INSTALLED_APPS
--------------

Aqui registramos las apps.

Ejemplo:

    INSTALLED_APPS = [
        ...
        "biblioteca",
    ]

Si una app no esta registrada, Django no la trata correctamente como parte
del proyecto.

DATABASES
---------

Indica que base de datos utilizamos.

Durante desarrollo es comun:

    SQLite

Pero Django tambien soporta PostgreSQL, MySQL y otros motores.

DEBUG
-----

Durante desarrollo:

    DEBUG = True

hace que Django muestre informacion detallada de los errores.

En produccion debe utilizarse:

    DEBUG = False

SECRET_KEY
----------

Es una clave utilizada por mecanismos de seguridad de Django.

No debe publicarse en repositorios cuando el proyecto sea real.

ALLOWED_HOSTS
-------------

Define los hosts/dominios desde los cuales se permite servir la aplicacion
cuando DEBUG esta desactivado.


================================================================
5. LA CARPETA PRINCIPAL Y LAS RUTAS
================================================================

Una aclaracion importante:

La carpeta del proyecto NO "controla todas las rutas" directamente.

El archivo:

    proyecto/urls.py

es el punto de entrada principal del sistema de URLs.

Puede delegar las rutas a las apps.

Ejemplo:

    proyecto/urls.py

    urlpatterns = [
        path("biblioteca/", include("biblioteca.urls")),
        path("estudiantes/", include("estudiantes.urls")),
    ]

Entonces:

    /biblioteca/
        -> biblioteca.urls

    /estudiantes/
        -> estudiantes.urls

Esto mantiene organizado el proyecto.


================================================================
6. urls.py
================================================================

urls.py contiene las rutas que Django puede reconocer.

Ejemplo:

    from django.urls import path
    from . import views

    urlpatterns = [
        path(
            "libros/",
            views.lista_libros,
            name="lista_libros"
        ),
    ]

La URL:

    /libros/

ejecutara:

    views.lista_libros


================================================================
7. path()
================================================================

path() conecta una URL con una view.

Forma general:

    path("ruta/", vista, name="nombre")

Ejemplo:

    path(
        "libros/",
        views.lista_libros,
        name="lista_libros"
    )

Tenemos:

    "libros/"
        -> patron de URL.

    views.lista_libros
        -> funcion que se ejecutara.

    name="lista_libros"
        -> nombre interno de la ruta.


================================================================
8. name EN path()
================================================================

name es MUY importante.

Ejemplo:

    path(
        "libros/",
        views.lista_libros,
        name="lista_libros"
    )

En un template:

    {% url "lista_libros" %}

Django buscara la ruta cuyo nombre sea:

    lista_libros

Esto es mejor que escribir:

    /biblioteca/libros/

directamente en todos los HTML.

Si despues cambiamos:

    "libros/"

por:

    "todos-los-libros/"

podemos mantener:

    name="lista_libros"

y los templates que utilizan:

    {% url "lista_libros" %}

seguirian funcionando.

IDEA CLAVE:

    path()
        define la ruta.

    name
        identifica la ruta dentro de Django.


================================================================
9. include()
================================================================

include() permite dividir las rutas.

Proyecto:

    proyecto/urls.py

    path(
        "biblioteca/",
        include("biblioteca.urls")
    )

Luego:

    biblioteca/urls.py

    urlpatterns = [
        path(
            "",
            views.biblioteca_dashboard,
            name="biblioteca"
        ),
        path(
            "libros/",
            views.lista_libros,
            name="lista_libros"
        ),
    ]

Resultado:

    /biblioteca/
        -> biblioteca_dashboard

    /biblioteca/libros/
        -> lista_libros

El prefijo:

    biblioteca/

lo agrega el urls.py principal.

La app solamente necesita definir:

    libros/


================================================================
10. PARAMETROS DINAMICOS EN path()
================================================================

Podemos meter valores dentro de la URL.

Ejemplo:

    path(
        "libros/<int:id>/",
        views.detalle_libro,
        name="detalle_libro"
    )

Si entramos a:

    /libros/15/

Django ejecuta:

    detalle_libro(request, id=15)

El:

    <int:id>

significa:

    int
        El valor debe ser un entero.

    id
        Nombre que recibira la view.

Otros convertidores:

    <str:nombre>
    <slug:slug>
    <uuid:id>
    <path:ruta>

Ejemplo:

    path(
        "programmer/<int:id>/",
        views.detalle_programmer,
        name="detalle_programmer"
    )


================================================================
11. namespaces Y app_name
================================================================

Cuando tenemos muchas apps pueden repetirse nombres.

Por ejemplo:

    biblioteca -> lista
    estudiantes -> lista

Podemos definir en biblioteca/urls.py:

    app_name = "biblioteca"

y luego:

    path(
        "libros/",
        views.lista_libros,
        name="lista"
    )

Ahora podemos utilizar:

    {% url "biblioteca:lista" %}

Esto evita conflictos.

IDEA:

    biblioteca:lista

significa:

    app biblioteca
    ruta lista


================================================================
12. EL FLUJO DE UNA PETICION
================================================================

Esta es probablemente la idea mas importante de Django.

Supongamos:

    GET /biblioteca/libros/

El navegador envia una peticion.

Django hace:

    1. Recibe HTTP Request.
    2. Busca en el urls.py principal.
    3. Encuentra "biblioteca/".
    4. Entra en biblioteca.urls.
    5. Encuentra "libros/".
    6. Ejecuta views.lista_libros.
    7. La view consulta el modelo.
    8. La view prepara un contexto.
    9. render() procesa el template.
    10. Django devuelve HTTP Response.
    11. El navegador muestra HTML.

Visualmente:

    navegador
        |
        v
    Request
        |
        v
    proyecto/urls.py
        |
        v
    biblioteca/urls.py
        |
        v
    views.lista_libros()
        |
        v
    Libro.objects.all()
        |
        v
    contexto
        |
        v
    template
        |
        v
    Response
        |
        v
    navegador


================================================================
13. VIEWS
================================================================

Una view recibe una peticion y decide que hacer.

Ejemplo:

    def inicio(request):
        return HttpResponse("Hola")

El parametro:

    request

contiene informacion de la peticion.

Por ejemplo:

    request.method
    request.GET
    request.POST
    request.user
    request.FILES
    request.session

Una view normalmente devuelve:

    HttpResponse
    render()
    redirect()
    JsonResponse()

o respuestas proporcionadas por otras herramientas.


================================================================
14. render()
================================================================

render() sirve para devolver un template HTML con datos.

Ejemplo:

    def lista_libros(request):

        libros = Libro.objects.all()

        return render(
            request,
            "biblioteca/listas.html",
            {
                "libros": libros
            }
        )

Tenemos:

    request
        -> peticion actual.

    "biblioteca/listas.html"
        -> template.

    {"libros": libros}
        -> contexto.


================================================================
15. CONTEXTO
================================================================

El contexto es informacion que enviamos desde Python hacia el template.

Ejemplo:

    return render(
        request,
        "biblioteca/listas.html",
        {
            "libros": libros,
            "titulo": "Mis libros"
        }
    )

En HTML:

    <h1>{{ titulo }}</h1>

    {% for libro in libros %}
        <p>{{ libro.titulo }}</p>
    {% endfor %}

Es decir:

    Python
        |
        | contexto
        v
    Template


================================================================
16. MODELOS
================================================================

Los modelos representan los datos de nuestra aplicacion.

Ejemplo:

    class Programmer(models.Model):
        fullname = models.CharField(max_length=100)
        nickname = models.CharField(max_length=100)
        language = models.CharField(max_length=100)
        age = models.IntegerField()
        is_active = models.BooleanField(default=True)

Este modelo describe la estructura de un Programmer.

Django utiliza esa informacion para trabajar con una tabla de la base
de datos.

RECOMENDACION:

Las clases normalmente se escriben con PascalCase:

    class Programmer(models.Model):

en vez de:

    class programmer(models.Model):

Aunque ambas formas pueden funcionar, PascalCase es la convencion
de Python.


================================================================
17. CAMPOS DE MODELOS
================================================================

Campos frecuentes:

    CharField
        Texto corto.

    TextField
        Texto largo.

    IntegerField
        Enteros.

    FloatField
        Decimales.

    DecimalField
        Decimales con precision.

    BooleanField
        True / False.

    DateField
        Fecha.

    DateTimeField
        Fecha y hora.

    EmailField
        Correo.

    ForeignKey
        Relacion muchos-a-uno.

    ManyToManyField
        Muchos-a-muchos.

    OneToOneField
        Uno-a-uno.


================================================================
18. primary_key
================================================================

Cada registro necesita una identificacion.

Django normalmente crea automaticamente un ID.

Tambien podemos definirlo:

    id_salon = models.AutoField(primary_key=True)

Ese campo sera la clave primaria.

La clave primaria identifica un registro de forma unica.


================================================================
19. max_length, default, null Y blank
================================================================

max_length:

    nombre = models.CharField(max_length=100)

Limita el texto.

default:

    activo = models.BooleanField(default=True)

Define un valor por defecto.

null:

    edad = models.IntegerField(null=True)

Permite NULL en la base de datos.

blank:

    edad = models.IntegerField(blank=True)

Permite que el valor quede vacio en validaciones/formularios.

IMPORTANTE:

    null
        principalmente relacionado con la base de datos.

    blank
        principalmente relacionado con validacion.


================================================================
20. RELACIONES ENTRE MODELOS
================================================================

Ejemplo:

    class Autor(models.Model):
        nombre = models.CharField(max_length=100)

    class Libro(models.Model):
        titulo = models.CharField(max_length=100)
        autor = models.ForeignKey(
            Autor,
            on_delete=models.CASCADE
        )

Tenemos:

    Autor 1 -------- N Libro

Un autor puede tener muchos libros.

El libro apunta a un autor mediante ForeignKey.


================================================================
21. on_delete
================================================================

Cuando utilizamos:

    ForeignKey(
        Autor,
        on_delete=models.CASCADE
    )

Django necesita saber que hacer cuando se elimina el autor.

CASCADE:

    eliminar Autor
        ->
    eliminar objetos relacionados.

PROTECT:

    impedir eliminacion si existen relaciones.

SET_NULL:

    colocar NULL si el campo permite null.

SET_DEFAULT:

    usar el valor por defecto.


================================================================
22. ORM
================================================================

ORM significa:

    Object-Relational Mapping

El ORM permite trabajar con la base de datos usando Python.

En lugar de escribir directamente:

    SELECT * FROM libro;

podemos escribir:

    Libro.objects.all()

Django genera la consulta correspondiente para la base de datos.

El ORM es una de las partes mas importantes de Django.


================================================================
23. objects.all()
================================================================

Ejemplo:

    libros = Libro.objects.all()

Obtiene todos los registros.

Normalmente devuelve un QuerySet.


================================================================
24. filter()
================================================================

Ejemplo:

    libros = Libro.objects.filter(
        is_active=True
    )

Obtiene los objetos que cumplen una condicion.

Puede devolver:

    0 objetos
    1 objeto
    muchos objetos


================================================================
25. get()
================================================================

Ejemplo:

    libro = Libro.objects.get(id=5)

Espera exactamente un objeto.

Si no existe:

    DoesNotExist

Si encuentra varios:

    MultipleObjectsReturned

Por eso no debemos utilizar get() cuando esperamos una lista.


================================================================
26. get_object_or_404()
================================================================

Ejemplo:

    from django.shortcuts import get_object_or_404

    libro = get_object_or_404(
        Libro,
        id=id
    )

Si existe:

    libro

Si no existe:

    respuesta HTTP 404

Es muy util para:

    detalle
    editar
    eliminar


================================================================
27. QuerySet
================================================================

Un QuerySet representa una consulta a la base de datos.

Ejemplo:

    libros = Libro.objects.filter(
        is_active=True
    )

Se pueden encadenar consultas:

    libros = (
        Libro.objects
        .filter(is_active=True)
        .order_by("titulo")
    )

Los QuerySets tienen evaluacion perezosa.

Esto significa que Django puede retrasar la ejecucion de la consulta
hasta que realmente necesita los resultados.


================================================================
28. OTROS METODOS DEL ORM
================================================================

Crear:

    Libro.objects.create(
        titulo="Django"
    )

Actualizar:

    libro.titulo = "Nuevo titulo"
    libro.save()

Eliminar:

    libro.delete()

Contar:

    Libro.objects.count()

Ordenar:

    Libro.objects.order_by("titulo")

Descendente:

    Libro.objects.order_by("-titulo")

Excluir:

    Libro.objects.exclude(is_active=False)


================================================================
29. MIGRACIONES
================================================================

Las migraciones conectan los cambios de models.py con la base de datos.

Cuando modificamos un modelo:

    class Libro(models.Model):
        titulo = ...
        paginas = ...

ejecutamos:

    python manage.py makemigrations

Despues:

    python manage.py migrate


================================================================
30. makemigrations VS migrate
================================================================

makemigrations:

    Modelo
       |
       v
    Detectar cambios
       |
       v
    Crear archivo de migracion

migrate:

    Archivo de migracion
       |
       v
    Ejecutar cambios
       |
       v
    Base de datos

Por eso:

    makemigrations

NO modifica directamente la base de datos.

Crea el plan.

    migrate

aplica el plan.


================================================================
31. migrations/
================================================================

Dentro de cada app normalmente existe:

    migrations/

Alli se guardan los cambios de estructura de la base de datos.

No deberiamos borrar migraciones sin saber exactamente que estamos haciendo.

En proyectos con Git, las migraciones normalmente se versionan.


================================================================
32. TEMPLATES
================================================================

Los templates son archivos HTML procesados por Django.

Ejemplo:

    biblioteca/
        templates/
            biblioteca/
                listas.html

Dentro:

    <h1>{{ titulo }}</h1>


================================================================
33. {{ }} VS {% %}
================================================================

    {{ variable }}

sirve principalmente para mostrar valores.

Ejemplo:

    {{ libro.titulo }}

En cambio:

    {% ... %}

se utiliza para instrucciones del template.

Ejemplos:

    {% for libro in libros %}
    {% if libro.is_active %}
    {% endif %}
    {% csrf_token %}
    {% url "lista_libros" %}
    {% extends "base.html" %}
    {% block content %}
    {% endblock %}


================================================================
34. for
================================================================

Ejemplo:

    {% for libro in libros %}
        <p>{{ libro.titulo }}</p>
    {% endfor %}

Tambien existe:

    {% empty %}

Ejemplo:

    {% for libro in libros %}
        <p>{{ libro.titulo }}</p>
    {% empty %}
        <p>No hay libros.</p>
    {% endfor %}


================================================================
35. if
================================================================

Ejemplo:

    {% if libro.is_active %}
        Activo
    {% else %}
        Inactivo
    {% endif %}


================================================================
36. HERENCIA DE TEMPLATES
================================================================

Esta es una de las herramientas mas importantes para evitar repeticion.

Creamos:

    base.html

Ejemplo:

    <!DOCTYPE html>
    <html>
    <head>
        <title>
            {% block title %}
            Mi sitio
            {% endblock %}
        </title>
    </head>

    <body>

        {% block content %}
        {% endblock %}

    </body>
    </html>

Luego:

    {% extends "base.html" %}

    {% block title %}
        Biblioteca
    {% endblock %}

    {% block content %}
        <h1>Biblioteca</h1>
    {% endblock %}


================================================================
37. POR QUE USAR base.html
================================================================

Sin herencia tendriamos que repetir:

    HTML
    navbar
    footer
    CSS
    scripts

en cada pagina.

Con herencia:

    base.html
       |
       +-- biblioteca/listas.html
       +-- biblioteca/formulario.html
       +-- biblioteca/confirmar_eliminar.html
       +-- estudiantes/lista.html

Si modificamos la navbar, la modificamos una vez.


================================================================
38. ESTRUCTURA DE TEMPLATES
================================================================

Una estructura recomendable:

    biblioteca/
        templates/
            biblioteca/
                biblioteca.html
                listas.html
                formulario.html
                confirmar_eliminar.html

La carpeta:

    biblioteca/

dentro de templates sirve para evitar conflictos.

Podemos tener:

    biblioteca/templates/biblioteca/listas.html

y:

    estudiantes/templates/estudiantes/listas.html

sin que sean el mismo archivo.


================================================================
39. {% load static %}
================================================================

Para utilizar archivos estaticos:

    {% load static %}

Despues:

    <link rel="stylesheet"
          href="{% static 'biblioteca/css/styles.css' %}">


================================================================
40. STATIC
================================================================

Static contiene archivos que pertenecen al proyecto:

    CSS
    JavaScript
    imagenes
    fuentes

Ejemplo:

    biblioteca/
        static/
            biblioteca/
                css/
                    styles.css
                js/
                    app.js
                img/
                    logo.png

En template:

    {% load static %}

    <link rel="stylesheet"
          href="{% static 'biblioteca/css/styles.css' %}">


================================================================
41. STATIC VS MEDIA
================================================================

STATIC:

    archivos del proyecto.

Ejemplo:

    CSS
    JS
    logo

MEDIA:

    archivos subidos por usuarios.

Ejemplo:

    foto de perfil
    documento
    imagen de producto subida por un usuario


================================================================
42. ERROR 404 DE CSS
================================================================

Si aparece:

    GET /static/css/styles.css 404

revisar:

    1. {% load static %}
    2. La ruta utilizada en {% static %}
    3. Que el archivo exista.
    4. Que STATIC_URL este configurado.
    5. Que la estructura static sea correcta.
    6. Que la app este instalada.
    7. Configuracion de desarrollo/produccion.

No confundir:

    URL de una pagina

con:

    URL de un archivo static.


================================================================
43. FORMULARIOS HTML
================================================================

Ejemplo:

    <form method="POST">

        {% csrf_token %}

        <input
            type="text"
            name="titulo"
        >

        <button type="submit">
            Guardar
        </button>

    </form>

El navegador envia los datos a la URL asociada al formulario.


================================================================
44. GET VS POST
================================================================

GET normalmente se utiliza para consultar informacion.

Ejemplo:

    /libros/?buscar=django

Los datos se obtienen mediante:

    request.GET

POST se utiliza normalmente para enviar datos que producen una accion.

Ejemplo:

    crear
    editar
    eliminar

Los datos se obtienen mediante:

    request.POST


================================================================
45. request.POST
================================================================

Si tenemos:

    <input type="text" name="titulo">

podemos hacer:

    titulo = request.POST.get("titulo")

Siempre debemos pensar en validar lo recibido.


================================================================
46. CSRF
================================================================

CSRF significa Cross-Site Request Forgery.

Django protege los formularios POST mediante un token.

Por eso normalmente escribimos:

    <form method="POST">
        {% csrf_token %}
        ...
    </form>

No se debe eliminar esta proteccion solamente para solucionar un error.


================================================================
47. CRUD
================================================================

CRUD significa:

    Create
    Read
    Update
    Delete

En español:

    Crear
    Leer
    Actualizar
    Eliminar

Para nuestra biblioteca:

    listas.html
        -> READ

    formulario.html
        -> CREATE / UPDATE

    confirmar_eliminar.html
        -> DELETE


================================================================
48. PATRON CRUD
================================================================

Un CRUD comun puede tener:

    lista
        mostrar registros.

    crear
        mostrar formulario y guardar.

    editar
        cargar objeto, mostrar formulario y guardar cambios.

    confirmar_eliminar
        pedir confirmacion.

    eliminar
        borrar y redirigir.


================================================================
49. CREAR Y EDITAR CON EL MISMO FORMULARIO
================================================================

Podemos reutilizar:

    formulario.html

Para crear:

    objeto no existe
        ->
    crear

Para editar:

    objeto existe
        ->
    editar

Podemos enviar:

    accion = "Crear"

o:

    accion = "Editar"

Y utilizar:

    <h1>
        {{ accion }} {{ config.singular }}
    </h1>

Esto reduce codigo repetido.


================================================================
50. redirect()
================================================================

redirect() envia al usuario hacia otra URL.

Ejemplo:

    return redirect("biblioteca:lista")

Muy comun despues de:

    crear
    editar
    eliminar

Patron:

    POST
      |
      v
    guardar
      |
      v
    redirect()
      |
      v
    GET lista


================================================================
51. POST -> REDIRECT -> GET
================================================================

Este patron es importante.

Ejemplo:

    Usuario envia formulario
          |
          v
        POST
          |
          v
    guardar objeto
          |
          v
       redirect
          |
          v
        GET
          |
          v
        lista

Esto evita que al refrescar el navegador se vuelva a enviar el formulario
POST.


================================================================
52. ELIMINACION Y CONFIRMACION
================================================================

No es recomendable eliminar objetos solamente porque alguien visito una URL
GET.

Mejor:

    GET
        muestra confirmacion.

    POST
        confirma y elimina.

Ejemplo conceptual:

    confirmar_eliminar.html
            |
            v
          POST
            |
            v
        objeto.delete()
            |
            v
         redirect()


================================================================
53. _meta
================================================================

Los modelos Django tienen informacion interna accesible mediante:

    objeto._meta

Ejemplos:

    objeto._meta.fields
    objeto._meta.get_fields()
    objeto._meta.model_name
    objeto._meta.verbose_name
    objeto._meta.verbose_name_plural

Esto es especialmente util cuando queremos crear vistas genericas.

Por ejemplo, en nuestros formularios dinamicos podemos recorrer:

    objeto._meta.fields

para conocer los campos de un modelo.


================================================================
54. VISTAS GENERICAS / CONFIGURACION DINAMICA
================================================================

Cuando tenemos muchos modelos:

    Libro
    Lector
    Autor
    Editorial
    Prestamo

podemos terminar repitiendo:

    listar
    crear
    editar
    eliminar

para cada modelo.

Una solucion es crear configuracion que describa cada modelo:

    nombre
    singular
    plural
    campos
    etc.

Luego las vistas utilizan esa configuracion.

Ventaja:

    menos codigo repetido.

Desventaja:

    mayor abstraccion.

IMPORTANTE:

Primero hay que entender el CRUD normal.

Despues tiene sentido crear abstracciones.


================================================================
55. NO TODO DEBE SER GENERICO
================================================================

No debemos intentar meter toda la aplicacion en una unica view gigantesca.

Por ejemplo:

    Autor
        tiene unas reglas.

    Prestamo
        puede tener fechas, devoluciones y reglas propias.

Aunque compartan CRUD, su logica de negocio puede ser diferente.

La reutilizacion debe simplificar el proyecto, no hacerlo incomprensible.


================================================================
56. FORMULARIOS DE DJANGO Y ModelForm
================================================================

Tambien existe:

    forms.py

Ejemplo:

    class LibroForm(forms.ModelForm):

        class Meta:
            model = Libro
            fields = "__all__"

ModelForm puede:

    crear campos automaticamente
    validar datos
    trabajar directamente con modelos
    mostrar errores

Para CRUD tradicionales suele ser mas robusto que procesar todo
manualmente con request.POST.


================================================================
57. VALIDACION
================================================================

Nunca hay que confiar ciegamente en:

    request.POST

Hay que validar:

    campos obligatorios
    tipos
    longitudes
    valores permitidos
    relaciones

ModelForm ayuda mucho en esto.

La base de datos tambien puede tener restricciones.


================================================================
58. DECORATORS
================================================================

Un decorator modifica o restringe el comportamiento de una funcion.

Ejemplo:

    @login_required

significa que normalmente solo usuarios autenticados pueden acceder
a esa view.

Otro ejemplo:

    @require_POST

puede exigir que una view solamente acepte POST.


================================================================
59. AUTENTICACION
================================================================

Django incluye un sistema de usuarios.

Permite manejar:

    usuarios
    contraseñas
    sesiones
    permisos
    grupos

Una view puede estar protegida:

    @login_required

Esto es importante en aplicaciones reales.


================================================================
60. MIDDLEWARE
================================================================

Middleware participa en el procesamiento de las peticiones y respuestas.

Conceptualmente:

    Request
       |
       v
    Middleware
       |
       v
    View
       |
       v
    Response
       |
       v
    Middleware
       |
       v
    Navegador

Puede encargarse de:

    seguridad
    sesiones
    autenticacion
    CSRF
    mensajes
    etc.

Middleware no es lo mismo que una view.


================================================================
61. MENSAJES
================================================================

Django tiene un sistema de mensajes.

Ejemplo:

    messages.success(
        request,
        "Libro creado correctamente."
    )

Puede servir para mostrar:

    creado correctamente
    actualizado correctamente
    eliminado correctamente
    error


================================================================
62. ADMIN
================================================================

Django incluye un panel administrativo.

Podemos registrar un modelo:

    from django.contrib import admin
    from .models import Libro

    admin.site.register(Libro)

Con un superusuario podemos gestionar registros.

Es muy util durante desarrollo para comprobar que los modelos funcionan.


================================================================
63. apps.py
================================================================

apps.py contiene la configuracion de la app.

Ejemplo:

    class BibliotecaConfig(AppConfig):
        default_auto_field = "django.db.models.BigAutoField"
        name = "biblioteca"

Normalmente no necesitamos modificarlo demasiado al principio.


================================================================
64. admin.py
================================================================

admin.py se utiliza principalmente para configurar el panel de
administracion de Django.

Ejemplo:

    from django.contrib import admin
    from .models import Libro

    admin.site.register(Libro)


================================================================
65. ASGI Y WSGI
================================================================

El proyecto normalmente contiene:

    asgi.py
    wsgi.py

Son puntos de entrada para servidores que ejecutan Django.

No necesitamos modificarlos normalmente cuando estamos aprendiendo.

La diferencia general:

    WSGI
        interfaz tradicional para aplicaciones web Python.

    ASGI
        interfaz mas moderna, pensada tambien para escenarios
        asincronos y conexiones de larga duracion.


================================================================
66. DJANGO REST FRAMEWORK
================================================================

Django REST Framework, o DRF, sirve para construir APIs sobre Django.

Django tradicional:

    navegador
        |
        v
    view
        |
        v
    template
        |
        v
    HTML

DRF:

    cliente
        |
        v
    API view / ViewSet
        |
        v
    serializer
        |
        v
    JSON


================================================================
67. API
================================================================

Una API permite que otros programas se comuniquen con nuestro backend.

Ejemplo:

    GET /api/programmers/

puede devolver:

    [
        {
            "id": 1,
            "fullname": "Juan",
            "language": "Python"
        }
    ]

El cliente puede ser:

    navegador
    React
    Next.js
    aplicacion movil
    otro servidor


================================================================
68. SERIALIZERS
================================================================

Un serializer transforma datos.

Conceptualmente:

    Modelo
       |
       v
    Serializer
       |
       v
    JSON

Tambien puede hacer el proceso inverso:

    JSON recibido
       |
       v
    Serializer
       |
       v
    datos validados
       |
       v
    Modelo


================================================================
69. VIEWSET Y ROUTER
================================================================

DRF permite utilizar ViewSets.

Un ViewSet puede reunir operaciones relacionadas con un recurso.

Un router puede generar automaticamente rutas.

Conceptualmente:

    router.register(
        "programmers",
        ProgrammerViewSet
    )

puede producir rutas para:

    listar
    crear
    consultar uno
    actualizar
    eliminar

Esto reduce codigo repetitivo.


================================================================
70. DJANGO HTML Y DRF PUEDEN CONVIVIR
================================================================

No hay que elegir necesariamente uno.

Podemos tener:

    /biblioteca/
        interfaz HTML.

    /api/programmers/
        API JSON.

El mismo proyecto puede servir:

    templates para humanos

y:

    APIs para otros programas.


================================================================
71. REDIRECCION DE UNA API A UNA VISTA HTML
================================================================

Si tenemos:

    /api/programmers/

y queremos que otra URL lleve al usuario a una pagina HTML, podemos utilizar
redirect().

Conceptualmente:

    URL A
      |
      v
    view
      |
      v
    redirect
      |
      v
    URL B


================================================================
72. ERRORES IMPORTANTES
================================================================

404 Page Not Found
------------------

Django no encontro una ruta o recurso.

Revisar:

    URL
    urls.py principal
    include()
    urls.py de app
    path()
    parametros


TemplateDoesNotExist
--------------------

Django no encuentra el HTML.

Revisar:

    nombre
    carpeta templates
    INSTALLED_APPS
    ruta utilizada en render()


NoReverseMatch
--------------

Django no pudo construir una URL.

Ejemplo:

    path(
        "libros/<int:id>/",
        views.detalle,
        name="detalle"
    )

Pero hacemos:

    {% url "detalle" %}

Falta:

    id

Deberia ser:

    {% url "detalle" libro.id %}


FieldError
----------

Estamos intentando utilizar un campo que no existe.


DoesNotExist
------------

get() no encontro el objeto.


IntegrityError
--------------

Se rompio una restriccion de la base de datos.


Method Not Allowed
------------------

La view no permite el metodo HTTP utilizado.


================================================================
73. COMO DEBUGGEAR
================================================================

No cambiar codigo al azar.

Seguir un orden.

1. Leer el error completo.
2. Mirar la URL que produjo el error.
3. Revisar urls.py.
4. Revisar la view.
5. Revisar el modelo.
6. Revisar el template.
7. Revisar static.
8. Revisar migraciones.
9. Revisar terminal.
10. Revisar base de datos.

Ejemplo:

    404

Primero:

    ¿La URL existe?

Despues:

    ¿El include() apunta a la app correcta?

Despues:

    ¿El path() esta bien?

Y recien despues revisar la view.


================================================================
74. PYTHON Y __pycache__
================================================================

Python crea:

    __pycache__/

y archivos:

    *.pyc

Son archivos temporales/compilados.

Normalmente no deben subirse a Git.

En .gitignore:

    __pycache__/
    *.pyc


================================================================
75. db.sqlite3 Y GIT
================================================================

Si utilizamos SQLite:

    db.sqlite3

contiene la base de datos local.

En muchos proyectos colaborativos se ignora:

    db.sqlite3

y se versionan:

    migrations/

porque las migraciones describen como construir la estructura de la
base de datos.

En un trabajo academico puede existir una decision distinta si se
necesita conservar datos de prueba.

La idea importante es entender la diferencia:

    migrations/
        estructura/cambios de la base.

    db.sqlite3
        datos de una base local.


================================================================
76. ENTORNO VIRTUAL
================================================================

Un entorno virtual aisla las dependencias del proyecto.

Crear:

    python -m venv env

Activar en Windows:

    env\Scripts\activate

Instalar Django:

    pip install django

Guardar dependencias:

    pip freeze > requirements.txt

Instalar despues:

    pip install -r requirements.txt


================================================================
77. requirements.txt
================================================================

Indica las dependencias Python que necesita el proyecto.

Por ejemplo:

    Django
    djangorestframework

y sus versiones correspondientes.

Esto permite que otra persona pueda instalar el entorno necesario.


================================================================
78. GIT Y DJANGO
================================================================

Normalmente se versionan:

    models.py
    views.py
    urls.py
    templates/
    static/
    migrations/
    admin.py
    forms.py
    serializers.py
    requirements.txt

Normalmente se ignoran:

    __pycache__/
    *.pyc
    env/
    .venv/
    db.sqlite3
    secretos

La decision exacta puede depender del proyecto.


================================================================
79. ESTRUCTURA COMPLETA DE EJEMPLO
================================================================

    proyecto/
    |
    +-- manage.py
    |
    +-- proyecto/
    |   +-- __init__.py
    |   +-- settings.py
    |   +-- urls.py
    |   +-- asgi.py
    |   +-- wsgi.py
    |
    +-- biblioteca/
    |   +-- migrations/
    |   +-- templates/
    |   |   +-- biblioteca/
    |   |       +-- biblioteca.html
    |   |       +-- listas.html
    |   |       +-- formulario.html
    |   |       +-- confirmar_eliminar.html
    |   |
    |   +-- static/
    |   |   +-- biblioteca/
    |   |       +-- css/
    |   |           +-- styles.css
    |   |
    |   +-- models.py
    |   +-- views.py
    |   +-- urls.py
    |   +-- admin.py
    |   +-- apps.py
    |   +-- forms.py
    |
    +-- api/
    |   +-- models.py
    |   +-- serializers.py
    |   +-- views.py
    |   +-- urls.py
    |
    +-- db.sqlite3
    +-- requirements.txt
    +-- .gitignore


================================================================
80. COMO CREAR UNA FUNCIONALIDAD NUEVA
================================================================

Cuando quieras agregar algo nuevo:

PASO 1
------

Pensar que datos necesita.

Ejemplo:

    Libro
        titulo
        autor
        editorial
        año


PASO 2
------

Crear/modificar el modelo.


PASO 3
------

Ejecutar:

    python manage.py makemigrations

y:

    python manage.py migrate


PASO 4
------

Crear la view.


PASO 5
------

Crear la URL.


PASO 6
------

Crear el template.


PASO 7
------

Conectar urls.py de la app con urls.py principal mediante include().


PASO 8
------

Agregar CSS/static si es necesario.


PASO 9
------

Probar.


PASO 10
-------

Agregar validacion, autenticacion y manejo de errores cuando corresponda.


================================================================
81. EJEMPLO COMPLETO: LISTAR
================================================================

MODELO:

    class Libro(models.Model):
        titulo = models.CharField(max_length=100)


VIEW:

    def lista_libros(request):

        libros = Libro.objects.all()

        return render(
            request,
            "biblioteca/listas.html",
            {
                "libros": libros
            }
        )


URL:

    path(
        "libros/",
        views.lista_libros,
        name="lista_libros"
    )


TEMPLATE:

    <h1>Libros</h1>

    {% for libro in libros %}
        <p>{{ libro.titulo }}</p>
    {% empty %}
        <p>No hay libros.</p>
    {% endfor %}


FLUJO:

    /biblioteca/libros/
          |
          v
    biblioteca.urls
          |
          v
    lista_libros()
          |
          v
    Libro.objects.all()
          |
          v
    contexto
          |
          v
    listas.html
          |
          v
    HTML


================================================================
82. EJEMPLO COMPLETO: CREAR
================================================================

Template:

    <form method="POST">
        {% csrf_token %}

        <input type="text" name="titulo">

        <button type="submit">
            Guardar
        </button>
    </form>


View conceptualmente:

    def crear_libro(request):

        if request.method == "POST":

            titulo = request.POST.get("titulo")

            Libro.objects.create(
                titulo=titulo
            )

            return redirect("lista_libros")

        return render(
            request,
            "biblioteca/formulario.html"
        )


Flujo:

    GET
        -> mostrar formulario.

    POST
        -> recibir datos.
        -> validar.
        -> crear objeto.
        -> redirect.


================================================================
83. EJEMPLO COMPLETO: EDITAR
================================================================

Flujo:

    URL:

        /libros/5/editar/

    Django obtiene:

        id = 5

    View:

        libro = get_object_or_404(
            Libro,
            id=id
        )

    GET:

        mostrar formulario con datos actuales.

    POST:

        recibir datos.
        validar.
        modificar libro.
        save().
        redirect.


================================================================
84. EJEMPLO COMPLETO: ELIMINAR
================================================================

Primero:

    libro = get_object_or_404(
        Libro,
        id=id
    )

Luego:

    libro.delete()

Finalmente:

    return redirect("lista_libros")

Idealmente:

    GET
        -> mostrar confirmacion.

    POST
        -> eliminar.


================================================================
85. SEPARACION DE RESPONSABILIDADES
================================================================

Intentar mantener:

    models.py
        datos y relaciones.

    views.py
        logica relacionada con requests/responses.

    urls.py
        rutas.

    templates/
        HTML.

    static/
        CSS/JS/imagenes.

    forms.py
        formularios y validacion.

    serializers.py
        datos de API.

No meter toda la aplicacion en views.py.


================================================================
86. QUE HACE CADA ARCHIVO
================================================================

manage.py
    Ejecutar comandos.

settings.py
    Configuracion.

urls.py
    Rutas.

models.py
    Estructura y acceso a datos.

views.py
    Logica de peticiones.

templates/
    HTML.

static/
    CSS/JS/imagenes del proyecto.

forms.py
    Formularios.

admin.py
    Panel admin.

apps.py
    Configuracion de la app.

serializers.py
    Transformacion/validacion de datos para API.

migrations/
    Historial de cambios de estructura de BD.


================================================================
87. QUE OCURRE AL PRESIONAR UN LINK
================================================================

HTML:

    <a href="{% url 'biblioteca:lista' %}">
        Ver libros
    </a>

El navegador solicita la URL.

Django:

    1. recibe request.
    2. busca URL.
    3. encuentra view.
    4. ejecuta view.
    5. consulta modelo.
    6. genera contexto.
    7. procesa template.
    8. devuelve response.
    9. navegador muestra HTML.


================================================================
88. QUE OCURRE AL ENVIAR UN FORMULARIO
================================================================

HTML:

    <form method="POST">
        {% csrf_token %}

        <input name="titulo">

        <button>
            Guardar
        </button>
    </form>

Flujo:

    Usuario
       |
       v
    POST
       |
       v
    URL
       |
       v
    View
       |
       v
    request.POST
       |
       v
    Validacion
       |
       v
    ORM
       |
       v
    Base de datos
       |
       v
    redirect
       |
       v
    Lista


================================================================
89. EL MAPA MENTAL DEFINITIVO
================================================================

                        NAVEGADOR
                            |
                            v
                       HTTP REQUEST
                            |
                            v
                    +----------------+
                    |    urls.py     |
                    +----------------+
                            |
                            v
                          VIEW
                         /    \
                        /      \
                       v        v
                    MODEL     TEMPLATE
                      |           |
                      v           |
                  DATABASE        |
                      |           |
                      +-------> CONTEXTO
                                  |
                                  v
                            HTML RESPONSE
                                  |
                                  v
                              NAVEGADOR


Para un formulario:

    TEMPLATE
        |
        | POST
        v
    URL
        |
        v
    VIEW
        |
        v
    request.POST
        |
        v
    VALIDACION
        |
        v
    MODEL / ORM
        |
        v
    DATABASE
        |
        v
    redirect()
        |
        v
    TEMPLATE


================================================================
90. ORDEN RECOMENDADO PARA APRENDER DJANGO
================================================================

Ya que los conceptos basicos estan aprendidos, el siguiente orden es bueno:

    1. HTTP basico.
    2. Proyecto vs app.
    3. settings.py.
    4. urls.py.
    5. path().
    6. include().
    7. parametros dinamicos.
    8. name y namespaces.
    9. views.
    10. request/response.
    11. render().
    12. contexto.
    13. templates.
    14. herencia.
    15. static.
    16. models.
    17. ORM.
    18. relaciones.
    19. migraciones.
    20. formularios.
    21. validacion.
    22. CRUD.
    23. autenticacion.
    24. decorators.
    25. middleware.
    26. testing.
    27. DRF.
    28. serializers.
    29. ViewSets.
    30. routers.
    31. APIs.
    32. despliegue.


================================================================
91. COSAS QUE DEBERIA PODER EXPLICAR SIN MIRAR
================================================================

    ¿Que diferencia hay entre proyecto y app?

    ¿Para que sirve settings.py?

    ¿Que hace urls.py?

    ¿Que hace path()?

    ¿Que diferencia hay entre URL y name?

    ¿Para que sirve include()?

    ¿Que son los parametros dinamicos?

    ¿Que es una view?

    ¿Que contiene request?

    ¿Que hace render()?

    ¿Que es contexto?

    ¿Que es un template?

    ¿Que diferencia hay entre {{ }} y {% %}?

    ¿Que hace extends?

    ¿Que son los blocks?

    ¿Que es static?

    ¿Que es un modelo?

    ¿Que es ORM?

    ¿Que diferencia hay entre all(), filter() y get()?

    ¿Que hace get_object_or_404()?

    ¿Que es un QuerySet?

    ¿Que es una ForeignKey?

    ¿Que hace on_delete?

    ¿Que son las migraciones?

    ¿Que diferencia hay entre makemigrations y migrate?

    ¿Que es CRUD?

    ¿Por que usar POST para acciones que modifican datos?

    ¿Para que sirve csrf_token?

    ¿Que hace redirect()?

    ¿Que es un decorator?

    ¿Que es middleware?

    ¿Que diferencia hay entre Django y DRF?

    ¿Que hace un serializer?

    ¿Que hace un router?


================================================================
92. CHECKLIST PARA CADA NUEVA FUNCIONALIDAD
================================================================

Antes de programar:

    [ ] ¿Que datos necesito?
    [ ] ¿Necesito un modelo?
    [ ] ¿Que URL tendra?
    [ ] ¿Que view la manejara?
    [ ] ¿Necesito GET o POST?
    [ ] ¿Necesito un template?
    [ ] ¿Necesito CSS/JS?
    [ ] ¿Necesito un formulario?
    [ ] ¿Necesito validacion?
    [ ] ¿Necesito autenticacion?
    [ ] ¿Necesito permisos?
    [ ] ¿Necesito migracion?
    [ ] ¿Necesito API?

Despues:

    [ ] Ejecutar servidor.
    [ ] Probar URL.
    [ ] Probar GET.
    [ ] Probar POST.
    [ ] Probar crear.
    [ ] Probar editar.
    [ ] Probar eliminar.
    [ ] Probar datos invalidos.
    [ ] Revisar errores de terminal.
    [ ] Revisar CSS/static.


================================================================
93. RESUMEN FINAL
================================================================

La arquitectura basica se puede recordar asi:

    URL
      |
      v
    VIEW
      |
      +------> MODEL / ORM
      |             |
      |             v
      |         DATABASE
      |
      v
    CONTEXTO
      |
      v
    TEMPLATE
      |
      v
    RESPONSE


Y una frase para memorizar:

    URL decide a donde va la peticion.
    VIEW decide que hacer.
    MODEL representa los datos.
    ORM permite trabajar con la base de datos.
    TEMPLATE muestra los datos.
    RESPONSE devuelve el resultado.


================================================================
94. IDEA FINAL
================================================================

No estudiar Django como una lista de comandos.

Cuando veas:

    path()

piensa:

    "Esta URL lleva a esta view."

Cuando veas:

    render()

piensa:

    "Esta view esta enviando datos a un HTML."

Cuando veas:

    Model.objects.filter(...)

piensa:

    "Estoy consultando la base de datos."

Cuando veas:

    {% url ... %}

piensa:

    "Estoy pidiendo a Django que construya una URL usando su name."

Cuando veas:

    {% extends ... %}

piensa:

    "Estoy reutilizando la estructura de otro template."

Cuando veas:

    {% static ... %}

piensa:

    "Estoy buscando un archivo CSS/JS/imagen gestionado como static."

Cuando veas:

    redirect()

piensa:

    "Termine esta accion y quiero mandar al usuario a otra URL."

Cuando veas:

    makemigrations

piensa:

    "Estoy preparando cambios de estructura."

Cuando veas:

    migrate

piensa:

    "Estoy aplicando esos cambios a la base de datos."

Y cuando algo falle:

    NO cambiar codigo al azar.

Seguir el camino:

    navegador
        ->
    URL
        ->
    VIEW
        ->
    MODEL / ORM
        ->
    TEMPLATE
        ->
    RESPONSE

La mayoria de los problemas que hemos encontrado se pueden ubicar
en alguno de esos puntos.

================================================================
FIN DE LA GUIA
================================================================
