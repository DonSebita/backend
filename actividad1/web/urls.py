from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quienes-somos/", views.quienes_somos, name="quienes_somos"),
    path("servicios/", views.servicios, name="servicios"),
    path("contacto/", views.contacto, name="contacto"),

    path(
        "programmers/",
        views.programmers,
        name="programmers"
    ),

    path(
        "programmers/create/",
        views.programmer_create,
        name="programmer_create"
    ),

    path(
        "programmers/<int:id>/update/",
        views.programmer_update,
        name="programmer_update"
    ),

    path(
        "programmers/<int:id>/delete/",
        views.programmer_delete,
        name="programmer_delete"
    ),
]