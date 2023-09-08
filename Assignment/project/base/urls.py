from django.urls import path
from .views import KeyValueAPIView

urlpatterns = [
    path('api/data/', KeyValueAPIView.as_view(), name='key-value-list'),
    path('api/data/<str:key>/', KeyValueAPIView.as_view(), name='key-value-detail'),
]
