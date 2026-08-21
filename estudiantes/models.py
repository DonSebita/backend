from django.db import models

# Create your models here.

class Salon(models.Model):
    """
    Representa el salón asignado (ej. 101, 201).
    """
    id_salon = models.IntegerField(primary_key=True, verbose_name="Número de Salón")

    class Meta:
        verbose_name = "Salón"
        verbose_name_plural = "Salones"

    def __str__(self):
        return f"Salón {self.id_salon}"


class Clase(models.Model):
    """
    Representa las asignaturas o materias (ej. Matemáticas, Biología).
    """
    nombre_clase = models.CharField(max_length=100, verbose_name="Nombre de la Clase")

    class Meta:
        verbose_name = "Clase"
        verbose_name_plural = "Clases"

    def __str__(self):
        return self.nombre_clase


class Estudiante(models.Model):
    """
    Representa a los estudiantes titulares.
    Se separan los campos no atómicos 'Nombre del titular' en 'titulo' y 'apellido'.
    """
    id_estudiante = models.IntegerField(primary_key=True, verbose_name="Número de Estudiante")
    titulo = models.CharField(max_length=20, verbose_name="Título/Tratamiento")  # Ej: Sr., Srita.
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name="estudiantes",
        verbose_name="Salón Asignado"
    )
    
    # Relación Muchos a Muchos (M:N) con Clase a través de una tabla intermedia explícita
    clases = models.ManyToManyField(
        Clase,
        through="EstudianteClase",
        related_name="estudiantes",
        verbose_name="Clases Inscritas"
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.titulo} {self.apellido} (#{self.id_estudiante})"


class EstudianteClase(models.Model):
    """
    Tabla intermedia / pivote que gestiona la relación M:N entre Estudiante y Clase.
    """
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Inscripción de Clase"
        verbose_name_plural = "Inscripciones de Clases"
        # Garantiza que un estudiante no se inscriba dos veces en la misma clase
        unique_together = ("estudiante", "clase")

    def __str__(self):
        return f"{self.estudiante} - {self.clase}"