from .views import PropertyApi

from django.urls import path

urlpatterns = [
    path('<int:property_id>/', PropertyApi.as_view(), name='property_with_property_id'),
    path('', PropertyApi.as_view(), name='property')
]
