from django.urls import path
from .views import (
    CartAPIView,
    CartItemDeleteAPIView,
    CheckoutAPIView,
    MisOrdenesAPIView,
    OrderStatusUpdateAPIView,
    CancellationRequestAPIView,
    CancellationDecisionAPIView,
)

urlpatterns = [
    # Carro de Matrícula
    path('carro/', CartAPIView.as_view(), name='carro-matricula'),
    path('carro/<int:pk>/', CartItemDeleteAPIView.as_view(), name='eliminar-item-carro'),

    # Transacciones
    path('ordenes/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('mis-ordenes/', MisOrdenesAPIView.as_view(), name='mis-ordenes'),

    # Gestión del Coordinador
    path('ordenes/<int:pk>/estado/', OrderStatusUpdateAPIView.as_view(), name='actualizar-estado-orden'),
   
    path(
        'ordenes/items/<int:pk>/solicitar-cancelacion/',
        CancellationRequestAPIView.as_view(),
        name='solicitar-cancelacion'
    ),

    # Aprobar/rechazar cancelación
    path(
        'ordenes/items/<int:pk>/cancelacion/',
        CancellationDecisionAPIView.as_view(),
        name='decision-cancelacion'
    ),
]