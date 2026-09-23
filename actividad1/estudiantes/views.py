from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Estudiante,
    EstudianteClase,
    Salon,
    Clase
)

# =========================
# INICIO ESTUDIANTES
# =========================

def estudiantes_home(request):
    return render(request, "estudiantes/home.html")


# =========================
# ESTUDIANTES
# =========================

def lista_estudiantes(request):
    estudiantes = (
        Estudiante.objects
        .select_related("salon")
        .prefetch_related("clases")
    )

    salones = Salon.objects.all()
    clases = Clase.objects.all()

    return render(request, "estudiantes/lista.html", {
        "estudiantes": estudiantes,
        "salones": salones,
        "clases": clases,
    })


def crear_estudiante(request):
    salones = Salon.objects.all()
    clases = Clase.objects.all()

    if request.method == "POST":
        estudiante = Estudiante.objects.create(
            id_estudiante=request.POST.get("id_estudiante"),
            titulo=request.POST.get("titulo"),
            apellido=request.POST.get("apellido"),
            salon_id=request.POST.get("salon")
        )

        clases_seleccionadas = request.POST.getlist("clases")

        for clase_id in clases_seleccionadas:
            EstudianteClase.objects.create(
                estudiante=estudiante,
                clase_id=clase_id
            )

        return redirect("lista_estudiantes")

    return render(request, "estudiantes/crear.html", {
        "salones": salones,
        "clases": clases
    })


def eliminar_estudiante(request, id_estudiante):

    estudiante = get_object_or_404(
        Estudiante,
        id_estudiante=id_estudiante
    )

    if request.method == "POST":
        estudiante.delete()

    return redirect("lista_estudiantes")

def editar_estudiante(request, id_estudiante):
    estudiante = get_object_or_404(
        Estudiante,
        id_estudiante=id_estudiante
    )

    if request.method == "POST":
        estudiante.titulo = request.POST.get("titulo")
        estudiante.apellido = request.POST.get("apellido")
        estudiante.salon_id = request.POST.get("salon")

        estudiante.save()

        # Actualizamos las clases
        clases_seleccionadas = request.POST.getlist("clases")

        EstudianteClase.objects.filter(
            estudiante=estudiante
        ).delete()

        for clase_id in clases_seleccionadas:
            EstudianteClase.objects.create(
                estudiante=estudiante,
                clase_id=clase_id
            )

        return redirect("lista_estudiantes")

    return redirect("lista_estudiantes")

# =========================
# SALONES
# =========================

def lista_salones(request):

    salones = Salon.objects.all()

    return render(
        request,
        "estudiantes/salones.html",
        {
            "salones": salones
        }
    )


def crear_salon(request):

    if request.method == "POST":

        id_salon = request.POST.get("id_salon")

        Salon.objects.create(
            id_salon=id_salon
        )

        return redirect("lista_salones")

    return render(
        request,
        "estudiantes/crear_salon.html"
    )

def editar_salon(request, id_salon):

    salon = get_object_or_404(
        Salon,
        id_salon=id_salon
    )

    if request.method == "POST":

        nuevo_id = request.POST.get("id_salon")

        salon.id_salon = nuevo_id
        salon.save()

        return redirect("lista_salones")

    return redirect("lista_salones")

def eliminar_salon(request, id_salon):
    salon = get_object_or_404(
        Salon,
        id_salon=id_salon
    )

    if request.method == "POST":
        salon.delete()

    return redirect("lista_salones")


# =========================
# CLASES
# =========================

def lista_clases(request):

    clases = Clase.objects.all()

    return render(
        request,
        "estudiantes/clases.html",
        {
            "clases": clases
        }
    )


def crear_clase(request):

    if request.method == "POST":

        nombre_clase = request.POST.get(
            "nombre_clase"
        )

        Clase.objects.create(
            nombre_clase=nombre_clase
        )

        return redirect("lista_clases")

    return render(
        request,
        "estudiantes/crear_clase.html"
    )

def editar_clase(request, id):

    clase = get_object_or_404(
        Clase,
        id=id
    )

    if request.method == "POST":

        clase.nombre_clase = request.POST.get(
            "nombre_clase"
        )

        clase.save()

        return redirect("lista_clases")

    return redirect("lista_clases")

def eliminar_clase(request, id):
    clase = get_object_or_404(
        Clase,
        id=id
    )

    if request.method == "POST":
        clase.delete()

    return redirect("lista_clases")
