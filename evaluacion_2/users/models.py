from django.contrib.auth.models import AbstractUser
from django.db import models

# =====================================================================
# Modelo de Usuario Personalizado
# Implementa los roles requeridos: Estudiante y Coordinador Académico.
# Hereda de AbstractUser para aprovechar la autenticación nativa de Django.
# =====================================================================
class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Estudiante'
        INSTRUCTOR='INSTRUCTOR', 'Instructor'
        COORDINATOR = 'COORDINATOR', 'Coordinador Académico'
    
    # Campo para definir el rol del usuario, por defecto es Estudiante.
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
