from django.db import models

class programmer(models.Model):
 fullname = models.CharField(max_length=100)
 nickname = models.CharField(max_length=100)
 language = models.CharField(max_length=100)
 age = models.PositiveSmallIntegerField()
 is_active = models.BooleanField(default=True)


class Lector(models.Model):
    CodLector = models.AutoField(primary_key=True)
    ApellidoP = models.CharField(max_length=100)
    ApellidoM = models.CharField(max_length=100)
    Nombres = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.ApellidoP} {self.ApellidoM}, {self.Nombres}"


class Libro(models.Model):
    CodLibro = models.AutoField(primary_key=True)
    Titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.Titulo


class Autor(models.Model):
    CodAutor = models.AutoField(primary_key=True)
    NombreAutor = models.CharField(max_length=150)

    def __str__(self):
        return self.NombreAutor


class Editorial(models.Model):
    CodEditorial = models.AutoField(primary_key=True)
    NombreEditorial = models.CharField(max_length=150)

    def __str__(self):
        return self.NombreEditorial


class Prestamo(models.Model):
    CodLibro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE
    )

    CodLector = models.ForeignKey(
        Lector,
        on_delete=models.CASCADE
    )

    FechaDev = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['CodLibro', 'CodLector'],
                name='unique_prestamo_libro_lector'
            )
        ]

    def __str__(self):
        return f"Préstamo de Libro {self.CodLibro} a Lector {self.CodLector}"


class Libro_Autor(models.Model):
    CodLibro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE
    )

    CodAutor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['CodLibro', 'CodAutor'],
                name='unique_libro_autor'
            )
        ]

    def __str__(self):
        return f"Libro {self.CodLibro} - Autor {self.CodAutor}"


class Libro_Editorial(models.Model):
    CodLibro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE
    )

    CodEditorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['CodLibro', 'CodEditorial'],
                name='unique_libro_editorial'
            )
        ]

    def __str__(self):
        return f"Libro {self.CodLibro} - Editorial {self.CodEditorial}"