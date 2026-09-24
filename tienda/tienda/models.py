from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'admin')
        extra_fields.setdefault('activo', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    id_usuario = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    # El campo 'password' ya está incluido internamente por AbstractBaseUser
    rol = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email' # Usaremos el email para el login con JWT
    
    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.email

class Cliente(models.Model):
    id_cliente = models.BigAutoField(primary_key=True)
    # Relación 1 a 1 según el diagrama
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    rut = models.CharField(max_length=9)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Empleado(models.Model):
    id_empleado = models.BigAutoField(primary_key=True)
    # Relación 1 a 1 para el empleado
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    rut = models.CharField(max_length=9)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    cargo = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'empleado'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    # Relación 1 a N: Un usuario puede tener muchas direcciones
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='direcciones')
    pais = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=20)
    sucursal = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=50)
    alias = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'direccion'

    def __str__(self):
        return f"{self.alias} - {self.direccion}"