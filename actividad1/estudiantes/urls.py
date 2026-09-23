from django.urls import path

from . import views


urlpatterns = [
    # Página principal del módulo
    path("", views.estudiantes_home, name="estudiantes_home"),

    # Estudiantes
    path(
        "lista/",
        views.lista_estudiantes,
        name="lista_estudiantes"
    ),

    path(
        "crear/",
        views.crear_estudiante,
        name="crear_estudiante"
    ),

    path(
        "<int:id_estudiante>/eliminar/",
        views.eliminar_estudiante,
        name="eliminar_estudiante"
    ),

    # Salones
    path(
        "salones/",
        views.lista_salones,
        name="lista_salones"
    ),

    path(
        "salones/crear/",
        views.crear_salon,
        name="crear_salon"
    ),

    path(
    "salones/<int:id_salon>/editar/",
    views.editar_salon,
    name="editar_salon"
    ),

    path(
        "salones/<int:id_salon>/eliminar/",
        views.eliminar_salon,
        name="eliminar_salon"
    ),

    # Clases
    path(
        "clases/",
        views.lista_clases,
        name="lista_clases"
    ),

    path(
        "clases/crear/",
        views.crear_clase,
        name="crear_clase"
    ),

    path(
    "clases/<int:id>/editar/",
    views.editar_clase,
    name="editar_clase"
    ),

    path(
        "clases/<int:id>/eliminar/",
        views.eliminar_clase,
        name="eliminar_clase"
    ),
    
    path(
    "<int:id_estudiante>/editar/",
    views.editar_estudiante,
    name="editar_estudiante"
),
]