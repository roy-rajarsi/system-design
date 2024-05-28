from .views import BookingApi

from django.urls import path

urlpatterns = [
    path('', BookingApi.as_view(), name='booking'),
]
