from drf_spectacular import views
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from courses.views import lista_cursos, detalle_curso
from edtech.views import (
    # Públicas
    index, login_view, register_view, logout_view, lista_cursos,error_404_view,
    # Estudiante
    estudiante_dashboard, estudiante_perfil, estudiante_carrito,
    carrito_agregar, carrito_eliminar, checkout_html, estudiante_mis_cursos,
    # Admin / Coordinador
    admin_dashboard,
    admin_cursos, admin_curso_nuevo, admin_curso_editar, admin_curso_eliminar,
    admin_areas, admin_area_nueva, admin_area_editar, admin_area_eliminar,
    admin_usuarios, admin_ordenes, admin_instructor_nuevo, admin_instructores,
    admin_instructor_editar,
    admin_instructor_eliminar,admin_usuario_nuevo,
    admin_usuario_editar,
    admin_usuario_eliminar,
)   

urlpatterns = [
    # ── Django Admin integrado ──────────────────────────────────────
    path('admin/', admin.site.urls),
    # ── Páginas públicas ────────────────────────────────────────────
    path('', index, name='index'),
    path('api/', include('enrollments.urls')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('cursos/', lista_cursos, name='lista_cursos'),
    path('cursos/<int:id>/', detalle_curso, name='detalle_curso'),

    # ── Panel Estudiante ────────────────────────────────────────────
    path('dashboard/', estudiante_dashboard, name='estudiante_dashboard'),
    path('perfil/', estudiante_perfil, name='estudiante_perfil'),
    path('carrito/', estudiante_carrito, name='estudiante_carrito'),
    path('carrito/agregar/<int:course_id>/', carrito_agregar, name='carrito_agregar'),
    path('carrito/eliminar/<int:item_id>/', carrito_eliminar, name='carrito_eliminar'),
    path('carrito/checkout/', checkout_html, name='checkout_html'),
    path('mis-cursos/', estudiante_mis_cursos, name='estudiante_mis_cursos'),

    # ── Panel Administrador / Coordinador ───────────────────────────
    path('panel/', admin_dashboard, name='admin_dashboard'),
    path('panel/cursos/', admin_cursos, name='admin_cursos'),
    path('panel/cursos/nuevo/', admin_curso_nuevo, name='admin_curso_nuevo'),
    path('panel/cursos/<int:pk>/editar/', admin_curso_editar, name='admin_curso_editar'),
    path('panel/cursos/<int:pk>/eliminar/', admin_curso_eliminar, name='admin_curso_eliminar'),
    path('panel/areas/', admin_areas, name='admin_areas'),
    path('panel/areas/nueva/', admin_area_nueva, name='admin_area_nueva'),
    path('panel/areas/<int:pk>/editar/', admin_area_editar, name='admin_area_editar'),
    path('panel/areas/<int:pk>/eliminar/', admin_area_eliminar, name='admin_area_eliminar'),
    path('panel/usuarios/', admin_usuarios, name='admin_usuarios'),
    path('panel/ordenes/', admin_ordenes, name='admin_ordenes'),

    path('panel/instructores/', admin_instructores, name='admin_instructores'),
    path('panel/instructores/nuevo/', admin_instructor_nuevo, name='admin_instructor_nuevo'),
    path('panel/instructores/<int:pk>/editar/',admin_instructor_editar,name='admin_instructor_editar'),
    path('panel/instructores/<int:pk>/eliminar/',admin_instructor_eliminar,name='admin_instructor_eliminar'),

    path('panel/usuarios/',admin_usuarios,name='admin_usuarios'),
    path('panel/usuarios/nuevo/',admin_usuario_nuevo,name='admin_usuario_nuevo'),
    path('panel/usuarios/<int:pk>/editar/', admin_usuario_editar, name='admin_usuario_editar'),
    path('panel/usuarios/<int:pk>/eliminar/', admin_usuario_eliminar, name='admin_usuario_eliminar'),

    # ── API REST (DRF) ──────────────────────────────────────────────
    path('api/auth/', include('users.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('enrollments.urls')),

    # ── Documentación OpenAPI / Swagger ─────────────────────────────
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    re_path(r'^.*$', error_404_view, name='error_404'),
]
