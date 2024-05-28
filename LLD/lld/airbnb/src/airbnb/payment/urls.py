from .views import PaymentApi

from django.urls import path

urlpatterns = [
    path('<int:order_id>/', PaymentApi.as_view(), name='payment_with_order_id'),
    path('', PaymentApi.as_view(), name='payment_with_order_id')
]
