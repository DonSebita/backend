from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Empleado,Usuario,Cliente,Direccion,Producto,Categoria
from .serializers import DireccionSerializer, ProductoSerializer, EmpleadoSerializer, ClienteSerializer, CategoriaSerializer

class HomeView(APIView):
    # Cualquiera puede ver el home sin iniciar sesión
    permission_classes = [AllowAny] 

    def get(self, request):
        return Response({
            "mensaje": "Bienvenido a la Tienda de Plantas",
            "estado": "El servidor está funcionando correctamente."
        })

class EsAdminOVendedor(BasePermission):
    """Permite el acceso solo a administradores y vendedores"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Verificamos si el rol es admin o vendedor
        return getattr(request.user, 'rol', '').lower() in ['admin', 'vendedor']

class EsSoloAdmin(BasePermission):
    """Permite el acceso exclusivo a administradores"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'rol', '').lower() == 'admin'
    
class PerfilClienteView(APIView):
    # Solo usuarios logueados con JWT pueden acceder
    permission_classes = [IsAuthenticated,EsSoloAdmin] 

    def get(self, request):
        try:
            # Buscamos el perfil del cliente asociado al usuario
            cliente = Cliente.objects.get(usuario=request.user)
            nombre_completo = f"{cliente.nombre} {cliente.apellido}".strip()
            telefono = cliente.telefono
        except Cliente.DoesNotExist:
            # Si el usuario es el superadmin y no tiene perfil de cliente creado
            nombre_completo = "Administrador"
            telefono = "No registrado"
        
        # Buscamos si el usuario tiene alguna dirección registrada
        direccion = request.user.direcciones.first()
        direccion_texto = f"{direccion.direccion}, {direccion.comuna}" if direccion else "No registrada"

        return Response({
            "usuario_id": request.user.id_usuario, # Corregido: 'id_usuario' en lugar de 'id'
            "username": nombre_completo,           # Corregido: Sacamos el nombre de la tabla Cliente
            "email": request.user.email,
            "telefono_contacto": telefono,
            "direccion_envio": direccion_texto
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
#direcciones
class DireccionClienteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Buscamos solo las direcciones que le pertenecen al usuario logueado
        direcciones = Direccion.objects.filter(usuario=request.user)
        serializer = DireccionSerializer(direcciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Copiamos los datos que envía el frontend y le asignamos el usuario actual internamente
        data = request.data.copy()
        data['usuario'] = request.user.id_usuario 
        
        serializer = DireccionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DireccionDetalleView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, usuario_id):
        try:
            # Buscamos la dirección asegurando que pertenezca al usuario logueado
            return Direccion.objects.get(pk=pk, usuario_id=usuario_id)
        except Direccion.DoesNotExist:
            return None

    def put(self, request, pk):
        direccion = self.get_object(pk, request.user.id_usuario)
        if not direccion:
            return Response({'error': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['usuario'] = request.user.id_usuario
        
        serializer = DireccionSerializer(direccion, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        direccion = self.get_object(pk, request.user.id_usuario)
        if not direccion:
            return Response({'error': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        direccion.delete()
        return Response({'mensaje': 'Eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)    

#productos

class ProductoListView(APIView):
    permission_classes = [IsAuthenticated, EsAdminOVendedor]

    def get(self, request):
        productos = Producto.objects.all().order_by('-id_producto')
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoDetalleView(APIView):
    permission_classes = [IsAuthenticated, EsAdminOVendedor]

    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None

    def put(self, request, pk):
        producto = self.get_object(pk)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.get_object(pk)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        producto.delete()
        return Response({'mensaje': 'Producto eliminado'}, status=status.HTTP_204_NO_CONTENT)
#categorias 

class CategoriaListView(APIView):
    permission_classes = [IsAuthenticated, EsAdminOVendedor]

    def get(self, request):
        categorias = Categoria.objects.all().order_by('nombre')
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaDetalleView(APIView):
    permission_classes = [IsAuthenticated, EsAdminOVendedor]

    def put(self, request, pk):
        try:
            categoria = Categoria.objects.get(pk=pk)
            serializer = CategoriaSerializer(categoria, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categoria.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            categoria = Categoria.objects.get(pk=pk)
            categoria.delete()
            return Response({'mensaje': 'Categoría eliminada'}, status=status.HTTP_204_NO_CONTENT)
        except Categoria.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)
#dashboard clientes y trabajadores

# --- VISTAS DE EMPLEADOS (TRABAJADORES) ---
class EmpleadoListView(APIView):
    permission_classes = [IsAuthenticated,EsSoloAdmin]
    
    def get(self, request):
        empleados = Empleado.objects.all().order_by('-id_empleado')
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        cargo = request.data.get('cargo', 'Bodeguero')
        
        # Validar si el correo ya existe
        if Usuario.objects.filter(email=email).exists():
            return Response({'error': 'El correo ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Creamos el Usuario base
        usuario = Usuario.objects.create_user(email=email, password=password, rol=cargo.lower())
        
        # 2. Creamos el perfil de Empleado
        empleado = Empleado.objects.create(
            usuario=usuario,
            nombre=request.data.get('nombre'),
            apellido=request.data.get('apellido'),
            rut=request.data.get('rut', ''),
            telefono=request.data.get('telefono', ''),
            cargo=cargo,
            estado=True
        )
        return Response(EmpleadoSerializer(empleado).data, status=status.HTTP_201_CREATED)

class EmpleadoDetalleView(APIView):
    permission_classes = [IsAuthenticated,EsSoloAdmin]

    def put(self, request, pk):
        try:
            empleado = Empleado.objects.get(pk=pk)
            empleado.nombre = request.data.get('nombre', empleado.nombre)
            empleado.apellido = request.data.get('apellido', empleado.apellido)
            empleado.rut = request.data.get('rut', empleado.rut)
            empleado.telefono = request.data.get('telefono', empleado.telefono)
            empleado.cargo = request.data.get('cargo', empleado.cargo)
            empleado.estado = request.data.get('estado', empleado.estado)
            empleado.save()
            
            # Actualizamos el rol en el usuario si el cargo cambió
            empleado.usuario.rol = empleado.cargo.lower()
            
            # Si se envió una nueva contraseña (por el doble clic), la actualizamos
            nueva_password = request.data.get('password')
            if nueva_password:
                empleado.usuario.set_password(nueva_password)
                
            empleado.usuario.save()
            return Response(EmpleadoSerializer(empleado).data)
        except Empleado.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            empleado = Empleado.objects.get(pk=pk)
            empleado.usuario.delete() # Esto elimina en cascada al empleado también
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Empleado.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# --- VISTAS DE CLIENTES ---
class ClienteListView(APIView):
    permission_classes = [IsAuthenticated,EsSoloAdmin]
    
    def get(self, request):
        clientes = Cliente.objects.all().order_by('-id_cliente')
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

class ClienteDetalleView(APIView):
    permission_classes = [IsAuthenticated,EsSoloAdmin]

    def put(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)
            cliente.nombre = request.data.get('nombre', cliente.nombre)
            cliente.apellido = request.data.get('apellido', cliente.apellido)
            cliente.rut = request.data.get('rut', cliente.rut)
            cliente.telefono = request.data.get('telefono', cliente.telefono)
            cliente.save()
            return Response(ClienteSerializer(cliente).data)
        except Cliente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        