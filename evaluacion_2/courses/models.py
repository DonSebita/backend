from django.db import models
from django.conf import settings
# =====================================================================
# Modelo de Área de Conocimiento
# Permite agrupar los cursos por categorías o áreas (ej. Desarrollo, Diseño).
# =====================================================================
class Area(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Nombre del área de conocimiento")
    description = models.TextField(blank=True, help_text="Descripción opcional del área")

    def __str__(self):
        return self.name

# =====================================================================
# Modelo de Curso / Bootcamp
# Representa la oferta académica. Maneja el costo, fechas y el inventario
# de cupos disponibles mediante 'max_capacity' y 'available_capacity'.
# Se agrega 'instructor' para darle un formato similar a Udemy.
# =====================================================================
class Course(models.Model):
    title = models.CharField(max_length=200, help_text="Título del curso o bootcamp")
    description = models.TextField(help_text="Descripción detallada del curso")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Apunta a 'users.User' de forma segura
        on_delete=models.RESTRICT, # Evita borrar a un instructor si tiene cursos asignados
        related_name='cursos_impartidos',
        limit_choices_to={'role': 'INSTRUCTOR'}, # Filtra automáticamente en los dropdowns
        null=True # Opcional: temporalmente True para que las migraciones no fallen con cursos antiguos
    )
    enrollment_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Costo de matrícula")
    start_date = models.DateField(help_text="Fecha de inicio")
    end_date = models.DateField(help_text="Fecha de término")
    
    max_capacity = models.PositiveIntegerField(help_text="Límite máximo de cupos por cohorte")
    # El stock físico disponible que será descontado atómicamente
    available_capacity = models.PositiveIntegerField(help_text="Cupos actualmente disponibles")
    
    area = models.ForeignKey(Area, related_name='courses', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Al crear el curso por primera vez, los cupos disponibles son iguales a la capacidad máxima
        if not self.pk and self.available_capacity is None:
            self.available_capacity = self.max_capacity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
