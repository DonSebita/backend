from django.urls import path, include
from rest_framework import routers
from api import views
from .views import (
    LibroViewSet, LectorViewSet, AutorViewSet,
    EditorialViewSet, PrestamoViewSet
)

router = DefaultRouter() 
router.register(r'programmers', views.ProgrammerViewSet)
router.register(r'libros', views.LIBROViewSet)
router.register(r'lectores', views.LectorViewSet)
router.register(r'autores', views.AutorViewSet)
router.register(r'editoriales', views.EditorialViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
