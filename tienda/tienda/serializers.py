from rest_framework import serializers
from .models import Usuario, Cliente, Empleado, Direccion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Evitamos enviar la contraseña en el JSON por seguridad
        fields = ['id_usuario', 'email', 'rol', 'activo', 'create_at', 'update_at']

class ClienteSerializer(serializers.ModelSerializer):
    # Anidamos el usuario para que el JSON del cliente traiga su email y rol
    usuario_detalle = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Empleado
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'