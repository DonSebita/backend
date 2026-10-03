from django.db import models
from django.conf import settings
from courses.models import Course

# =====================================================================
# Modelo de Carro de Matrícula (Cart)
# Relación 1 a 1 con el Usuario. Almacena temporalmente los cursos antes
# del checkout. Es persistente en la base de datos (PostgreSQL).
# =====================================================================
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carro de {self.user.username}"

# =====================================================================
# Modelo de Ítem del Carro (CartItem)
# Relaciona los cursos agregados con un carro específico.
# Implementa la regla de negocio: no se puede agregar el mismo curso
# dos veces al mismo carro (unique_together).
# =====================================================================
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Restricción para evitar duplicados en el carro
        unique_together = ('cart', 'course')

    def __str__(self):
        return f"{self.course.title} en carro de {self.cart.user.username}"

# =====================================================================
# Modelo de Orden / Transacción (Order)
# Representa el registro histórico tras el checkout.
# Implementa explícitamente CHOICES para el estado de la transacción,
# cumpliendo con la exigencia de la pauta.
# =====================================================================
from django.db import models
from django.conf import settings


class Order(models.Model):

    class Status(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    class CancellationStatus(models.TextChoices):
        NONE = 'NONE', 'Sin solicitud'
        REQUESTED = 'REQUESTED', 'Solicitud pendiente'
        REJECTED = 'REJECTED', 'Solicitud rechazada'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDIENTE
    )

    cancellation_status = models.CharField(
        max_length=20,
        choices=CancellationStatus.choices,
        default=CancellationStatus.NONE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(
            item.price_at_purchase
            for item in self.items.all()
        )

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username} ({self.status})"
# =====================================================================
# Modelo de Ítem de la Orden (OrderItem)
# Congela el precio del curso al momento de la compra (price_at_purchase)
# para evitar que cambios futuros en el catálogo afecten el histórico.
# =====================================================================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Usamos PROTECT para no eliminar un curso si ya tiene órdenes asociadas
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.course.title} (Orden #{self.order.id})"
