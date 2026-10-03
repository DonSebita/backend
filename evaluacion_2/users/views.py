from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

# =====================================================================
# Vista para generar el Token JWT
# Usa nuestro serializador personalizado que inyecta el 'role'.
# =====================================================================
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer