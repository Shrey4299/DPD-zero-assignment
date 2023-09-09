from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('api/', include('base.urls')),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]
