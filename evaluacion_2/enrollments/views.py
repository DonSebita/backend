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
            return Response(
                {"error": "El course_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        if CartItem.objects.filter(
            cart=cart,
            course=course
        ).exists():
            return Response(
                {"error": "El curso ya está en el carro de matrícula."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = CartItem.objects.create(
            cart=cart,
            course=course
        )

        serializer = CartItemSerializer(item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

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

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart or not cart.items.exists():
            return Response(
                {"error": "El carro de matrícula está vacío."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                status=Order.Status.PENDIENTE
            )

            for item in cart.items.all():

                OrderItem.objects.create(
                    order=order,
                    course=item.course,
                    price_at_purchase=item.course.enrollment_cost
                )

            cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

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

        # ==========================================
        # Verificar permisos
        # Superusuario o Coordinador
        # ==========================================

        if not request.user.is_superuser and request.user.role != 'COORDINATOR':

            return Response(
                {
                    "error":
                    "Acceso denegado. Se requiere rol de Coordinador Académico o Superusuario."
                },
                status=status.HTTP_403_FORBIDDEN
            )


        # ==========================================
        # Buscar orden
        # ==========================================

        order = get_object_or_404(
            Order,
            pk=pk
        )


        # ==========================================
        # Obtener nuevo estado
        # ==========================================

        new_status = request.data.get('status')


        # ==========================================
        # Validar estado
        # ==========================================

        if new_status not in dict(Order.Status.choices):

            return Response(
                {
                    "error":
                    f"Estado inválido. Opciones: "
                    f"{list(dict(Order.Status.choices).keys())}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # ==========================================
        # Evitar cambiar al mismo estado
        # ==========================================

        if order.status == new_status:

            return Response(
                {
                    "error":
                    "La orden ya tiene ese estado."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            with transaction.atomic():

                # ==========================================
                # PENDIENTE → PAGADO
                # ==========================================

                if (
                    new_status == Order.Status.PAGADO
                    and order.status == Order.Status.PENDIENTE
                ):

                    for item in order.items.all():

                        course = Course.objects.select_for_update().get(
                            id=item.course.id
                        )


                        # Verificar cupos
                        if course.available_capacity < 1:

                            raise ValueError(
                                f"No hay cupos disponibles para "
                                f"'{course.title}'."
                            )


                        # Descontar cupo
                        course.available_capacity -= 1

                        course.save()


                # ==========================================
                # PAGADO → CANCELADO
                # ==========================================

                elif (
                    new_status == Order.Status.CANCELADO
                    and order.status == Order.Status.PAGADO
                ):

                    for item in order.items.all():

                        course = Course.objects.select_for_update().get(
                            id=item.course.id
                        )

                        # Devolver cupo
                        course.available_capacity += 1

                        course.save()


                # ==========================================
                # PENDIENTE → CANCELADO
                # ==========================================

                elif (
                    new_status == Order.Status.CANCELADO
                    and order.status == Order.Status.PENDIENTE
                ):

                    # No se modifica el cupo
                    pass


                # ==========================================
                # Guardar estado
                # ==========================================

                order.status = new_status

                order.save()


        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # ==========================================
        # Respuesta
        # ==========================================

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class CancellationRequestAPIView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        order = get_object_or_404(
            Order,
            pk=pk,
            user=request.user
        )

        # Solo se puede solicitar cancelar una matrícula PAGADA
        if order.status != Order.Status.PAGADO:
            return Response(
                {
                    "error": "Solo puedes solicitar la cancelación de matrículas pagadas."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ya existe una solicitud
        if (
            order.cancellation_status
            == Order.CancellationStatus.REQUESTED
        ):
            return Response(
                {
                    "error": "Ya existe una solicitud de cancelación pendiente."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.cancellation_status = (
            Order.CancellationStatus.REQUESTED
        )

        order.save()

        serializer = OrderSerializer(order)

        return Response(
            {
                "message": "Solicitud de cancelación enviada correctamente.",
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )

class CancellationDecisionAPIView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):

        # Solo Coordinador o SuperAdmin

        if (
            not request.user.is_superuser
            and request.user.role != 'COORDINATOR'
        ):
            return Response(
                {
                    "error": (
                        "Se requiere rol de Coordinador "
                        "Académico o Superusuario."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )


        order = get_object_or_404(
            Order,
            pk=pk
        )


        # Verificar solicitud

        if (
            order.cancellation_status
            != Order.CancellationStatus.REQUESTED
        ):
            return Response(
                {
                    "error": (
                        "Esta orden no tiene una "
                        "solicitud de cancelación pendiente."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        decision = request.data.get('decision')


        if decision not in ['APPROVE', 'REJECT']:

            return Response(
                {
                    "error": (
                        "La decisión debe ser "
                        "APPROVE o REJECT."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            with transaction.atomic():

                # =========================================
                # APROBAR
                # =========================================

                if decision == 'APPROVE':

                    if order.status != Order.Status.PAGADO:

                        raise ValueError(
                            "La orden ya no se encuentra pagada."
                        )


                    for item in order.items.all():

                        course = Course.objects.select_for_update().get(
                            id=item.course.id
                        )

                        # Devolver cupo

                        course.available_capacity += 1

                        course.save()


                    order.status = Order.Status.CANCELADO

                    order.cancellation_status = (
                        Order.CancellationStatus.NONE
                    )


                    order.save()


                # =========================================
                # RECHAZAR
                # =========================================

                elif decision == 'REJECT':

                    order.cancellation_status = (
                        Order.CancellationStatus.REJECTED
                    )

                    order.save()


        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )