from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'programmers', views.ProgrammerViewSet)
router.register(r'libros', views.LibroViewSet)
router.register(r'lectores', views.LectorViewSet)
router.register(r'autores', views.AutorViewSet)
router.register(r'editoriales', views.EditorialViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
