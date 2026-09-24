from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario,Cliente

class HomeView(APIView):
    # Cualquiera puede ver el home sin iniciar sesión
    permission_classes = [AllowAny] 

    def get(self, request):
        return Response({
            "mensaje": "Bienvenido a la Tienda de Plantas",
            "estado": "El servidor está funcionando correctamente."
        })

class PerfilClienteView(APIView):
    # Solo usuarios logueados con JWT pueden acceder
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # Buscamos o creamos el perfil del cliente automáticamente
        cliente, created = Cliente.objects.get_or_create(usuario=request.user)
        
        return Response({
            "usuario_id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "telefono_contacto": cliente.telefono_contacto,
            "direccion_envio": cliente.direccion_envio
        })

# Vistas para los Templates (Frontend)
class HomeTemplateView(TemplateView):
    template_name = 'tienda/home.html'

class LoginTemplateView(TemplateView):
    template_name = 'tienda/login.html'

class PerfilTemplateView(TemplateView):
    template_name = 'tienda/perfil.html'

def error_404_view(request, *args, **kwargs):
    # Renderiza el template 404 y devuelve el código de error 404
    return redirect('web_home')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['rol'] = self.user.rol # Añadimos el rol al JSON de respuesta
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 2. Vista de API para Registrar Clientes
class RegistroClienteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        nombre = request.data.get('nombre', '')
        apellido = request.data.get('apellido', '')

        if Usuario.objects.filter(email=email).exists():
            return Response({'error': 'El email ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

        # Creamos el usuario base y el perfil de cliente asociado
        usuario = Usuario.objects.create_user(email=email, password=password, rol='cliente')
        Cliente.objects.create(usuario=usuario, nombre=nombre, apellido=apellido, rut="", telefono="")
        
        return Response({'mensaje': 'Cuenta creada con éxito'}, status=status.HTTP_201_CREATED)

# 3. Vista de Template para el Dashboard del Admin
class AdminDashboardTemplateView(TemplateView):
    template_name = 'tienda/admin_dashboard.html'