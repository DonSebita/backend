from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.biblioteca_dashboard,
        name="biblioteca"
    ),

    path(
        "<str:modelo>/crear/",
        views.crear,
        name="biblioteca_crear"
    ),

    path(
        "<str:modelo>/<int:pk>/editar/",
        views.editar,
        name="biblioteca_editar"
    ),

    path(
        "<str:modelo>/<int:pk>/eliminar/",
        views.eliminar,
        name="biblioteca_eliminar"
    ),

    path(
        "<str:modelo>/",
        views.lista,
        name="biblioteca_lista"
    ),
]