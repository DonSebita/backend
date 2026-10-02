from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Area, Course
from .serializers import AreaSerializer, CourseSerializer

# =====================================================================
# Permiso Personalizado (RBAC)
# - Métodos seguros (GET) son de acceso público.
# - Métodos de escritura requieren que el usuario sea COORDINADOR.
# =====================================================================
class IsCoordinatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role == 'COORDINATOR')

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsCoordinatorOrReadOnly]

# =====================================================================
# ViewSet de Cursos
# Implementa django-filter para búsquedas por área, fechas y costo.
# =====================================================================
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsCoordinatorOrReadOnly]
    
    # Sistema de filtros requerido por la rúbrica
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area', 'start_date', 'enrollment_cost']
