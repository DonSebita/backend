from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from courses.models import Course
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer

# =====================================================================
# Gestión del Carro de Matrícula
# Protegido por IsAuthenticated. Relación 1:1 persistente.
# =====================================================================
class CartAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart = self.get_cart(request.user)
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({"error": "El course_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, id=course_id)
        
        # Validar que no se dupliquen cursos en el mismo carro
        if CartItem.objects.filter(cart=cart, course=course).exists():
            return Response({"error": "El curso ya está en el carro de matrícula."}, status=status.HTTP_400_BAD_REQUEST)
            
        item = CartItem.objects.create(cart=cart, course=course)
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemDeleteAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# =====================================================================
# Transacción / Checkout
# Bloque atómico que genera la orden, valida el cupo en tiempo real,
# lo descuenta y vacía el carro.
# =====================================================================
class CheckoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"error": "El carro de matrícula está vacío."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Iniciamos bloque atómico para que, si algo falla, no se descuente nada
            with transaction.atomic():
                order = Order.objects.create(user=request.user, status=Order.Status.PAGADO)
                
                for item in cart.items.all():
                    course = item.course
                    # select_for_update() bloquea la fila temporalmente previniendo sobreventas (race conditions)
                    course_locked = Course.objects.select_for_update().get(id=course.id)
                    
                    if course_locked.available_capacity < 1:
                        raise ValueError(f"No hay cupos disponibles para matricularse en '{course.title}'.")
                    
                    # Descuento atómico del inventario
                    course_locked.available_capacity -= 1
                    course_locked.save()
                    
                    # Se congela el precio histórico
                    OrderItem.objects.create(
                        order=order,
                        course=course,
                        price_at_purchase=course.enrollment_cost
                    )
                
                # Vaciar el carro luego de procesar todos los ítems
                cart.items.all().delete()
                
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# =====================================================================
# Historial de Órdenes del Estudiante
# =====================================================================
class MisOrdenesAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

# =====================================================================
# Gestión de Estados para el Coordinador
# Si cancela una matrícula, el cupo debe liberarse y reponerse.
# =====================================================================
class OrderStatusUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        # Protegemos el endpoint para que solo el rol COORDINATOR pueda cambiar estados
        if request.user.role != 'COORDINATOR':
            return Response({"error": "Acceso denegado. Se requiere rol de Coordinador Académico."}, status=status.HTTP_403_FORBIDDEN)
            
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.Status.choices):
            return Response({"error": f"Estado inválido. Opciones: {list(dict(Order.Status.choices).keys())}"}, status=status.HTTP_400_BAD_REQUEST)
            
        if order.status != new_status:
            with transaction.atomic():
                # Lógica de reposición de cupos si se cancela una orden ya pagada
                if new_status == Order.Status.CANCELADO and order.status == Order.Status.PAGADO:
                    for item in order.items.all():
                        course = Course.objects.select_for_update().get(id=item.course.id)
                        course.available_capacity += 1
                        course.save()
                        
                order.status = new_status
                order.save()
                
        serializer = OrderSerializer(order)
        return Response(serializer.data)
