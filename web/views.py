from django.shortcuts import render, get_object_or_404, redirect
from api.models import programmer,Libro, Lector, Autor, Editorial, Prestamo
from .forms import ProgrammerForm


def home(request):
    return render(request, "web/home.html")


def programmers(request):
    lista_programmers = programmer.objects.all()

    form = ProgrammerForm()

    return render(
        request,
        "web/programmers.html",
        {
            "programmers": lista_programmers,
            "form": form,
        }
    )


def programmer_create(request):
    if request.method == "POST":
        form = ProgrammerForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect("programmers")


def programmer_update(request, id):
    prog = get_object_or_404(programmer, id=id)

    if request.method == "POST":

        prog.fullname = request.POST.get("fullname")
        prog.nickname = request.POST.get("nickname")
        prog.language = request.POST.get("language")
        prog.age = request.POST.get("age")

        prog.is_active = (
            request.POST.get("is_active") == "True"
        )

        prog.save()

    return redirect("programmers")

def programmer_delete(request, id):
    prog = get_object_or_404(programmer, id=id)

    if request.method == "POST":
        prog.delete()

    return redirect("programmers")

def quienes_somos(request):
    return render(request, "web/quienes_somos.html")


def servicios(request):
    return render(request, "web/servicios.html")


def contacto(request):
    return render(request, "web/contacto.html")

def biblioteca_view(request):
    libros = Libro.objects.all()
    lectores = Lector.objects.all()
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    prestamos = Prestamo.objects.select_related('CodLibro', 'CodLector').all()

    context = {
        'libros': libros,
        'lectores': lectores,
        'autores': autores,
        'editoriales': editoriales,
        'prestamos': prestamos,
    }
    return render(request, 'web/biblioteca.html', context)