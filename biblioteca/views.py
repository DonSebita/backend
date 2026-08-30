from django.shortcuts import render
from api.models import Libro, Lector, Autor, Editorial, Prestamo


def biblioteca_dashboard(request):
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
