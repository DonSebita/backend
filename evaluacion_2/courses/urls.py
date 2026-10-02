from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AreaViewSet, CourseViewSet

router = DefaultRouter()
router.register(r'areas', AreaViewSet)
router.register(r'cursos', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
