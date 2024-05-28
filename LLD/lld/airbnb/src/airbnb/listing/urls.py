from .views import ListingApi

from django.urls import path

urlpatterns = [
    path("<int:listing_id>/", ListingApi.as_view(), name='listing_with_id'),
    path('', ListingApi.as_view(), name='listing'),
]
