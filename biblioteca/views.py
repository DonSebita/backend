from django.shortcuts import render, redirect, get_object_or_404
from api.models import (
    Lector,
    Libro,
    Autor,
    Editorial,
    Prestamo,
    Libro_Autor,
    Libro_Editorial,
)


# ==========================================================
# CONFIGURACIÓN DE LOS MODELOS
# ==========================================================

MODELOS = {
    "lectores": {
        "modelo": Lector,
        "nombre": "Lectores",
        "singular": "Lector",
        "titulo": "Gestión de Lectores",
    },
    "libros": {
        "modelo": Libro,
        "nombre": "Libros",
        "singular": "Libro",
        "titulo": "Gestión de Libros",
    },
    "autores": {
        "modelo": Autor,
        "nombre": "Autores",
        "singular": "Autor",
        "titulo": "Gestión de Autores",
    },
    "editoriales": {
        "modelo": Editorial,
        "nombre": "Editoriales",
        "singular": "Editorial",
        "titulo": "Gestión de Editoriales",
    },
    "prestamos": {
        "modelo": Prestamo,
        "nombre": "Préstamos",
        "singular": "Préstamo",
        "titulo": "Gestión de Préstamos",
    },
    "libro_autor": {
        "modelo": Libro_Autor,
        "nombre": "Libros - Autores",
        "singular": "Relación Libro - Autor",
        "titulo": "Gestión de Libros y Autores",
    },
    "libro_editorial": {
        "modelo": Libro_Editorial,
        "nombre": "Libros - Editoriales",
        "singular": "Relación Libro - Editorial",
        "titulo": "Gestión de Libros y Editoriales",
    },
}


# ==========================================================
# DASHBOARD PRINCIPAL
# ==========================================================

def biblioteca_dashboard(request):

    libros = Libro.objects.all()
    lectores = Lector.objects.all()
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    prestamos = Prestamo.objects.all()

    context = {
        "libros": libros,
        "lectores": lectores,
        "autores": autores,
        "editoriales": editoriales,
        "prestamos": prestamos,
    }

    return render(
        request,
        "biblioteca/biblioteca.html",
        context
    )


# ==========================================================
# LISTAR
# ==========================================================

def lista(request, modelo):

    config = MODELOS.get(modelo)

    if not config:
        return redirect("biblioteca")

    Model = config["modelo"]

    objetos = Model.objects.all()

    context = {
        "objetos": objetos,
        "config": config,
        "modelo": modelo,
    }

    return render(
        request,
        "biblioteca/lista.html",
        context
    )


# ==========================================================
# CREAR
# ==========================================================

def crear(request, modelo):

    config = MODELOS.get(modelo)

    if not config:
        return redirect("biblioteca")

    Model = config["modelo"]

    campos = Model._meta.fields

    if request.method == "POST":

        datos = {}

        for campo in campos:

            if campo.primary_key:
                continue

            nombre = campo.name

            if campo.is_relation:
                valor = request.POST.get(nombre)

                if valor:
                    datos[nombre + "_id"] = valor

            else:
                valor = request.POST.get(nombre)

                if campo.get_internal_type() == "BooleanField":
                    datos[nombre] = nombre in request.POST
                else:
                    datos[nombre] = valor

        Model.objects.create(**datos)

        return redirect(
            "biblioteca_lista",
            modelo=modelo
        )

    context = {
        "config": config,
        "modelo": modelo,
        "accion": "Crear",
        "objeto": None,
        "campos": campos,
    }

    return render(
        request,
        "biblioteca/formulario.html",
        context
    )

# ==========================================================
# EDITAR
# ==========================================================

def editar(request, modelo, pk):

    config = MODELOS.get(modelo)

    if not config:
        return redirect("biblioteca")

    Model = config["modelo"]

    objeto = get_object_or_404(
        Model,
        pk=pk
    )

    campos = Model._meta.fields

    if request.method == "POST":

        for campo in campos:

            if campo.primary_key:
                continue

            nombre = campo.name

            if campo.is_relation:

                valor = request.POST.get(nombre)

                if valor:
                    setattr(
                        objeto,
                        nombre + "_id",
                        valor
                    )

            else:

                valor = request.POST.get(nombre)

                if campo.get_internal_type() == "BooleanField":
                    setattr(
                        objeto,
                        nombre,
                        nombre in request.POST
                    )
                else:
                    setattr(
                        objeto,
                        nombre,
                        valor
                    )

        objeto.save()

        return redirect(
            "biblioteca_lista",
            modelo=modelo
        )

    context = {
        "config": config,
        "modelo": modelo,
        "accion": "Editar",
        "objeto": objeto,
        "campos": campos,
    }

    return render(
        request,
        "biblioteca/formulario.html",
        context
    )

# ==========================================================
# ELIMINAR
# ==========================================================

def eliminar(request, modelo, pk):

    config = MODELOS.get(modelo)

    if not config:
        return redirect("biblioteca")

    Model = config["modelo"]

    objeto = get_object_or_404(
        Model,
        pk=pk
    )

    if request.method == "POST":

        objeto.delete()

        return redirect(
            "biblioteca_lista",
            modelo=modelo
        )

    context = {
        "config": config,
        "modelo": modelo,
        "objeto": objeto,
    }

    return render(
        request,
        "biblioteca/confirmar_eliminar.html",
        context
    )