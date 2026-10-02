from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# =====================================================================
# Vista para generar el Token JWT
# Usa nuestro serializador personalizado que inyecta el 'role'.
# =====================================================================
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
