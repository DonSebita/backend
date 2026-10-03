from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Area, Course
from .serializers import AreaSerializer, CourseSerializer


class IsCoordinatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'COORDINATOR'
        )


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsCoordinatorOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsCoordinatorOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area', 'start_date', 'enrollment_cost']


# Lista de cursos
def lista_cursos(request):
    courses = Course.objects.all()

    return render(
        request,
        'cursos/lista.html',
        {'courses': courses}
    )


# Detalle de un curso
def detalle_curso(request, id):
    course = get_object_or_404(Course, id=id)

    return render(
        request,
        'cursos/detalle.html',
        {'course': course}
    )