from django.urls import path
from .views import (
    CartAPIView, 
    CartItemDeleteAPIView, 
    CheckoutAPIView, 
    MisOrdenesAPIView, 
    OrderStatusUpdateAPIView
)

urlpatterns = [
    # Carro de Matrícula
    path('api/carro/', CartAPIView.as_view(), name='carro-matricula'),
    path('api/carro/<int:pk>/', CartItemDeleteAPIView.as_view(), name='eliminar-item-carro'),
    
    # Transacciones
    path('api/ordenes/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('api/mis-ordenes/', MisOrdenesAPIView.as_view(), name='mis-ordenes'),
    
    # Gestión del Coordinador
    path('api/ordenes/<int:pk>/estado/', OrderStatusUpdateAPIView.as_view(), name='actualizar-estado-orden'),
]
