from django.urls import path
from .views import KeyValueAPIView

urlpatterns = [
    path('data/', KeyValueAPIView.as_view(), name='key-value-list'),
    path('data/<str:key>/', KeyValueAPIView.as_view(), name='key-value-detail'),
]
