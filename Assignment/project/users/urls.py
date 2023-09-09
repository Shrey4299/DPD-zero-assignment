from django.urls import path
from .views import CustomUserCreate, LoginView, UserView
app_name = 'users'

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('token/', LoginView.as_view(), name="login_user"),
    path('user/', UserView.as_view(), name="user"),

]
