from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# =====================================================================
# Serializador de Usuario
# =====================================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

# =====================================================================
# Serializador JWT Personalizado (Requisito de Pauta)
# Incluye el 'rol' del usuario (claims) dentro del payload del token.
# =====================================================================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añadimos el claim personalizado
        token['role'] = user.role
        return token
