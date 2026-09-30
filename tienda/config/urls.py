from django.contrib import admin
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from tienda.views import (
    HomeView, PerfilClienteView, RegistroClienteView, CustomLoginView,
    HomeTemplateView, LoginTemplateView, PerfilTemplateView, AdminDashboardTemplateView,
    error_404_view, DireccionClienteView, DireccionDetalleView, ProductoListView, ProductoDetalleView, EmpleadoListView, EmpleadoDetalleView,
    ClienteListView, ClienteDetalleView, CategoriaListView, CategoriaDetalleView
)

urlpatterns = [
    path('admin/', admin.site.urls), # Admin predeterminado de Django
    
    # --- RUTAS FRONTEND (Templates) ---
    path('', HomeTemplateView.as_view(), name='web_home'),
    path('login/', LoginTemplateView.as_view(), name='web_login'),
    path('perfil/', PerfilTemplateView.as_view(), name='web_perfil'),
    path('admin-dashboard/', AdminDashboardTemplateView.as_view(), name='web_admin_dashboard'),

    # --- RUTAS BACKEND (API) ---
    path('api/home/', HomeView.as_view(), name='api_home'),
    path('api/perfil/', PerfilClienteView.as_view(), name='api_perfil'),
    path('api/registro/', RegistroClienteView.as_view(), name='api_registro'),
    
    # Usamos nuestro CustomLoginView en lugar del genérico
    path('api/login/', CustomLoginView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),

    path('api/direcciones/', DireccionClienteView.as_view(), name='api_direcciones'),
    path('api/direcciones/<int:pk>/', DireccionDetalleView.as_view(), name='api_direccion_detalle'),

    path('api/productos/', ProductoListView.as_view(), name='api_productos'),
    path('api/productos/<int:pk>/', ProductoDetalleView.as_view(), name='api_producto_detalle'),

    path('api/categorias/', CategoriaListView.as_view(), name='api_categorias'),
    path('api/categorias/<int:pk>/', CategoriaDetalleView.as_view(), name='api_categoria_detalle'),

    path('api/empleados/', EmpleadoListView.as_view(), name='api_empleados'),
    path('api/empleados/<int:pk>/', EmpleadoDetalleView.as_view(), name='api_empleado_detalle'),
    path('api/clientes/', ClienteListView.as_view(), name='api_clientes'),
    path('api/clientes/<int:pk>/', ClienteDetalleView.as_view(), name='api_cliente_detalle'),

    re_path(r'^.*$', error_404_view, name='error_404'),
]